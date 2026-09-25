import json


def load_json(path):
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def build_edited_facts(dataset):
    facts = set()
    for item in dataset:
        for rewrite in item["requested_rewrite"]:
            prompt = rewrite["prompt"].format(rewrite["subject"])
            facts.add(f'{prompt} {rewrite["target_new"]["str"]}')
    return list(facts)


def build_questions(dataset):
    return [item["questions"][0] for item in dataset]


def construct_similar_qa(dataset, questions, index):
    result = f"Question: {questions[index]}\nReasoning process:\n"
    steps = [
        f"[STEP] {hop['cloze']} {hop['answer']}"
        for hop in dataset[index]["new_single_hops"]
    ]
    return result + "\n".join(steps)


def construct_first_similar_qa(dataset, questions, index):
    hop = dataset[index]["new_single_hops"][0]
    return f"Question: {questions[index]}\n[STEP] {hop['cloze']} {hop['answer']}"
