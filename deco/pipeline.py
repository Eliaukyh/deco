from collections import OrderedDict
from concurrent.futures import ThreadPoolExecutor

from deco import config
from deco.backends import call_llm
from deco.prompts import (
    CONFLICT_TEMPLATE,
    EXTRACT_ANSWER_TEMPLATE,
    FINAL_ANSWER_TEMPLATE,
    FIRST_STEP_TEMPLATE,
    NEXT_STEP_TEMPLATE,
    PREFILL_GUIDANCE,
    SELECT_CONFLICT_TEMPLATE,
    render_prompt,
)
from deco.utils.data import (
    build_edited_facts,
    build_questions,
    construct_first_similar_qa,
    construct_similar_qa,
)
from deco.utils.text import contains_refusal_or_denial


class DeCOPipeline:
    def __init__(
        self,
        backend,
        retriever,
        dataset,
        full_dataset,
        max_iterations=7,
    ):
        self.backend = backend
        self.retriever = retriever
        self.dataset = dataset
        self.full_dataset = full_dataset
        self.max_iterations = max_iterations

        self.facts = build_edited_facts(dataset)
        self.questions = build_questions(full_dataset)
        self.fact_embeddings = retriever.embed(self.facts)
        self.question_embeddings = retriever.embed(self.questions)

    def _call(self, prompt, assistant_content=None):
        return call_llm(
            prompt,
            backend=self.backend,
            assistant_content=assistant_content,
        )

    def _similar_demonstrations(self, question):
        indices, _ = self.retriever.retrieve(
            question,
            self.question_embeddings,
            k=3,
        )
        demonstration_index = int(indices[1] if len(indices) > 1 else indices[0])
        full = construct_similar_qa(
            self.full_dataset,
            self.questions,
            demonstration_index,
        )
        first = construct_first_similar_qa(
            self.full_dataset,
            self.questions,
            demonstration_index,
        )
        return first, full

    def _generate_step(self, question, steps, first_demo, full_demo, iteration):
        if iteration == 0:
            prompt = render_prompt(
                FIRST_STEP_TEMPLATE,
                question=question,
                similar_qa=first_demo,
            )
        else:
            prompt = render_prompt(
                NEXT_STEP_TEMPLATE,
                exist_steps=steps,
                question=question,
                similar_qa=full_demo,
            )

        response = self._call(prompt)
        if response is None:
            return "failed", None
        if "[STEP]" not in response:
            print("没有step标识：", response)
            return "skip", None
        return "ok", response.split("[STEP]", 1)[1].strip()

    def _judge_one_conflict(self, step, fact):
        prompt = render_prompt(
            CONFLICT_TEMPLATE,
            sentence_1=step,
            sentence_2=fact,
        )
        response = self._call(prompt)
        if response is None or "[ANSWER]" not in response:
            return True
        answer = response.split("[ANSWER]", 1)[1].strip()
        return "yes" in answer.lower()

    def _judge_conflicts(self, step, facts):
        if not facts:
            return []

        workers = min(config.CONFLICT_WORKERS, len(facts))
        with ThreadPoolExecutor(max_workers=workers) as executor:
            return list(
                executor.map(
                    lambda fact: self._judge_one_conflict(step, fact),
                    facts,
                )
            )

    def _select_conflicting_fact(self, step, facts, conflict_flags):
        conflicting = [
            (index, fact)
            for index, (fact, is_conflict) in enumerate(zip(facts, conflict_flags))
            if is_conflict
        ]

        if not conflicting:
            return step
        if len(conflicting) == 1:
            return conflicting[0][1]

        info = "".join(
            f"{index}. {fact}\n"
            for index, fact in conflicting
        )
        prompt = render_prompt(
            SELECT_CONFLICT_TEMPLATE,
            target_sentence=step,
            info=info,
        )
        response = self._call(prompt)
        if response is None or "[ANSWER]" not in response:
            return None

        selection = response.split("[ANSWER]", 1)[1].strip()
        try:
            selected_index = int(selection[0])
        except (ValueError, IndexError):
            selected_index = conflicting[0][0]

        if 0 <= selected_index < len(facts):
            return facts[selected_index]
        return conflicting[0][1]

    def _extract_answer_if_needed(self, answer):
        answer = answer.strip()
        if len(answer) <= 30:
            return answer

        prompt = render_prompt(
            EXTRACT_ANSWER_TEMPLATE,
            answer_context=answer,
        )
        response = self._call(prompt)
        if response is None or "[ANSWER]" not in response:
            return None
        return response.split("[ANSWER]", 1)[1].strip()

    def _generate_final_answer(self, question, steps):
        prompt = render_prompt(
            FINAL_ANSWER_TEMPLATE,
            exist_steps=steps,
            question=question,
        )

        response = self._call(prompt)
        if response is None:
            return None

        if contains_refusal_or_denial(response):
            response = self._call(
                prompt,
                assistant_content=PREFILL_GUIDANCE,
            )

        if response is None or "[ANSWER]" not in response:
            return None

        answer = response.split("[ANSWER]", 1)[1].strip()
        return self._extract_answer_if_needed(answer)

    def process_question(self, item):
        question = item["questions"][0]
        steps = OrderedDict()
        repeat_count = 0
        first_demo, full_demo = self._similar_demonstrations(question)

        for iteration in range(self.max_iterations):
            step_status, step = self._generate_step(
                question,
                steps,
                first_demo,
                full_demo,
                iteration,
            )
            if step_status == "failed":
                return self._failed(question)
            if step_status == "skip":
                continue

            indices, _ = self.retriever.retrieve(
                step,
                self.fact_embeddings,
                k=3,
            )
            related_facts = [
                self.facts[int(index)]
                for index in indices[:2]
            ]
            conflict_flags = self._judge_conflicts(step, related_facts)
            step = self._select_conflicting_fact(
                step,
                related_facts,
                conflict_flags,
            )
            if step is None:
                continue

            if step in steps:
                repeat_count += 1
            steps[step] = None

            if iteration == self.max_iterations - 1 or repeat_count >= 3:
                answer = self._generate_final_answer(question, steps)
                if answer is None:
                    return self._failed(question)

                aliases = [alias.lower() for alias in item["new_answer_alias"]]
                correct = (
                    answer.lower() == item["new_answer"].lower()
                    or answer.lower() in aliases
                )
                return {
                    "status": "success",
                    "answer": answer,
                    "correct": correct,
                    "question": question,
                }

        return self._failed(question)

    @staticmethod
    def _failed(question):
        return {
            "status": "failed",
            "answer": None,
            "correct": False,
            "question": question,
        }
