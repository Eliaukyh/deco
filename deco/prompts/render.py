def render_prompt(
    template,
    exist_steps=None,
    question=None,
    sentence_1=None,
    sentence_2=None,
    similar_qa=None,
    answer_context=None,
    info=None,
    target_sentence=None,
):
    if exist_steps is None:
        steps = "None"
    else:
        steps = "\n".join(exist_steps.keys())

    values = {
        "<exist_steps>": steps,
        "<question>": question,
        "<first_sentence>": sentence_1,
        "<second_sentence>": sentence_2,
        "<similar_question>": similar_qa,
        "<ans_context>": answer_context,
        "<info>": info,
        "<target_sentence>": target_sentence,
    }

    prompt = template
    for placeholder, value in values.items():
        if value is not None:
            prompt = prompt.replace(placeholder, value)
    return prompt
