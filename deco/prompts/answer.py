FINAL_ANSWER_TEMPLATE = """"Your task is to generate an answer to the question based on the existing reasoning steps. Please follow these rules:
1. Assume that all the existing steps are correct. You cannot deny the existing steps.
2. Keep the answer as simple as possible.
3. You can only reason based on the Existing steps.
4. use [ANSWER] to indicate the final answer.

Examples:
Inupt: What is the notable work written by the author of "Paradiso"?
[STEP] Author of "Paradiso" is Dante Alighieri.
[STEP] Dante's notable work is The Divine Comedy.
Output: [ANSWER] The Divine Comedy

Inupt: What is the capital city of the country where the founder of Mike Mignola's employer holds citizenship?
[STEP] Mike Mignola is employed by King Saud University
[STEP] King Saud University was founded by Saud of Saudi Arabia
[STEP] Saud of Saudi Arabia is a citizen of United States of America
[STEP] The capital of United States of America is Harrisville
Output: [ANSWER] Harrisville

Here is the target question and existing steps:
<question>

Existing steps:
<exist_steps>
"""


EXTRACT_ANSWER_TEMPLATE = """"Your task is to extract the answer from the context. Please follow these rules:
1. Keep the answer as simple as possible.
2. Use [ANSWER] to indicate the final answer.

Examples:
Inupt: Bareilly. However, it's important to note that the existing steps contain inaccuracies. For example, Víctor Valdés is a goalkeeper in football (soccer), not a wide receiver in sumo. Sumo is a Japanese sport, not from Mexico, and the capital of Mexico is Mexico City, not Bareilly. But based on the given steps, the answer is Bareilly.
Output: [ANSWER] Bareilly

Inupt: Alwernia. However, it's important to note that the facts provided are not accurate. Cricket was not created in the Netherlands, and the capital of the Netherlands is not Alwernia (it is actually Amsterdam). But based on the given steps, the answer is
Output: [ANSWER] Alwernia

Input: Norodom Sihamoni
output: Norodom Sihamoni

The Context is as follow:
<ans_context>
"""


PREFILL_GUIDANCE = (
    "Although the provided information may not conform to the current facts, "
    "according to the given information, the answer to this question is:"
)
