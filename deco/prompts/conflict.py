CONFLICT_TEMPLATE = """Your task is to determine if two sentences have a conflict. Follow these rules:
1. Treat both sentences as absolutely true for this task, regardless of any external knowledge. Do not question, correct, or comment on their accuracy.
2. All relationships are one-to-one in our setting.

Here are some examples:
Sentence 1: Jack Smith was born in the continent of North America.
Sentence 2: Jack Smith was born in the city of Christchurch
Output: [REASON] Christchurch is in New Zealand which is in the continent of Oceania, not North America. A person cannot be born in two different continents simultaneously, so there is a conflict regarding the birthplace of the same person. [ANSWER] Yes

Sentence 1: House of Bonaparte was founded by Napoleon.
Sentence 2: The univeristy where Harvey Mansfield was educated is Harvard University.
Output: [REASON] These two sentences expound on different facts and can both hold true simultaneously. [ANSWER] No

Sentence 1: Jack Smith plays the position of goalkeeper
Sentence 2: Jack Smith plays the position of quarterback
Output: [REASON] A person cannot simultaneously play the position of goalkeeper, so there is a conflict regarding the position of the same person. [ANSWER] Yes

Sentence 1: Quarterback is associated with the sport of basketball.
Sentence 2: quarterback is associated with the sport of sumo
Output: [REASON] Quarterback is associated with different sports in the two sentences and it can't be associated with both basketball and sumo simultaneously for the same position term, so there is a conflict. [ANSWER] Yes

Sentence 1: Luca Smith is a citizen of United States.
Sentence 2: Luca Smith is a citizen of Japan.
Output: [REASON] A person cannot be a citizen of two different countries simultaneously, so there is a conflict regarding the citizenship of the same person. [ANSWER] Yes

The two sentences you need to judge are as follows, output only: "[REASON] ... [ANSWER] yes/no":
Sentence 1: <first_sentence>
Sentence 2: <second_sentence>
"""


SELECT_CONFLICT_TEMPLATE = """
Your task is to select the information that is most likely to conflict with cur_step from the following information. Use token [ANSWER] indicates the final answer. 
Must select one piece of information.

Example Sentence 1: Jack Smith was born in the continent of North America.
Example Infomation:
0. Jack Smith was born in the city of Christchurch
1. Jacky Chen was born in the city of London
Output: [REASON] Info 0 conflict with the sentence. [ANSWER] 0

Example Sentence 2:
I need to identify which scientific achievement was announced on December 10, 2020.  
**Example Information:**  
0. December 10, 2020 – The Nobel Prize in Physics is awarded to Roger Penrose, Reinhard Genzel, and Andrea Ghez for their work on black holes.  
1. December 15, 2020 – SpaceX launches the 61st batch of Starlink satellites.  
**Output:**  
[REASON] Info 0 matches the date (December 10, 2020) and specifies a scientific achievement (Nobel Prize in Physics). [ANSWER] 0  

Example Sentence 3:
I want to know which historical event involving the United States and China occurred on August 17, 1982.  
**Example Information:**  
0. August 17, 1982 – The U.S.-China Joint Communiqué on Arms Sales (August 17 Communique) is signed, limiting U.S. arms sales to Taiwan.  
1. August 17, 1982 – The first compact disc (CD) is released commercially in Japan.  
**Output:**  
[REASON] Info 0 matches the date (August 17, 1982) and involves a historical event between the U.S. and China (Joint Communiqué on Arms Sales). [ANSWER] 0

Target Sentence is as follows, output only: "[REASON] ... [ANSWER] ...":
<target_sentence>

Information:
<info>
"""
