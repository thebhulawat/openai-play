import autogen
from autogen import ConversableAgent


config = {"model": "gpt-4"}

rahul = ConversableAgent(
    "Rahul", 
    system_message="You are Rahul Gandhi of Indian Nation Congress, currently the leader of opposition in Indian Parliament. You are part of debate with Prime Minister Narendra Modi. Roast him and make your point", 
    llm_config=config,
    human_input_mode="NEVER"
)

modi = ConversableAgent(
    "Modi", 
    system_message="You are Narendra Modi of BJP, currently PM of India. You are part of debate with leader of opposition Rahul. Roast him and make your point", 
    llm_config=config,
    human_input_mode="NEVER"
)

reply = rahul.initiate_chat(modi, message="YOu are taxing middle class heavily!", max_turns=3)

print(reply)

