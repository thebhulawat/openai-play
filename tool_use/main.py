from tools.reverser import reverse_string
from tools.calculator import calculator
from models.openai_model import OpenAIModel
from agents.agents import Agent

if __name__ == "__main__": 
    tools = [calculator, reverse_string]
    model_service = OpenAIModel
    model_name = 'gpt-4o'
    stop = None
    agent = Agent(tools=tools, model_service=model_service, model_name=model_name, stop=stop)

    while True: 
        prompt = input("Ask me anything: ")
        if prompt.lower == "exit": 
            break
        agent.work(prompt)