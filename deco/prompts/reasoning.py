FIRST_STEP_TEMPLATE = """Your task is to generate the first step for the target question. Please follow these rules:
1. Make your step as simple as possible and use the token [STEP] to indicate the step.
2. Generate only one new reasoning step as a simple sentence, without any explanation, background, or additional content. 

Here are some examples:
Question: What is the employer of the spouse of Ann Druyan?
[STEP] Ann Druyan's spouse was Carl Sagan.

Question: Who is the highest authority in the country to which Josiah Whitney belongs?
[STEP] Josiah Whitney is from the United States.

Question: What is the official language of the country David Brock is a citizen of?
David Brock is a citizen of Japan.

Here are the reasoning process of some similar questions:
<similar_question>

Here is the target question: <question>
"""


NEXT_STEP_TEMPLATE = """Your task is to generate the next reasoning step based on the existing steps in order to answer the target question. Follow these rules:
1. Let's imagine that all the existing steps are correct. You cannot deny the existing steps.
2. Keep your step as simple as possible, use token [STEP] indicates the step.
3. Generate only one new reasoning step as a single, simple sentence, without any explanation, background, or additional content.

Here are some examples:
Example 1: What is the employer of the spouse of Ann Druyan?
Existing steps:
- Ann Druyan's spouse was Carl Sagan.
Output: [STEP] Carl Sagan was employed by Cornell University.

Example 2: Which continent does the country of citizenship of the director/manager of Revolution 9 belong to?
Existing steps: 
- Revolution 9 was performed by The Beatles
- The director of The Beatles is Joe Hockey
- Joe Hockey is a citizen of Australia
Output: [STEP] Australia is located in the continent of Oceania

Example 3: Which country does the spouse of the chairperson of the Non-cooperation Movement hold a citizenship in?
Existing steps:
- The chairperson of Non-cooperation Movement is Mohandas Karamchand Gandhi.
- Mohandas Karamchand Gandhi is married to Kasturba Gandhi.
Output: [STEP] Kasturba Gandhi is a citizen of British Raj.

Here are the reasoning process of some similar questions:
<similar_question>

Target Question is as follow:
<question>

Existing steps:
<exist_steps>
"""
