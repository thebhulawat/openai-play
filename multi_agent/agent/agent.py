from openai import OpenAI
import openai
from state.state import State

class Agent:
    def __init__(self, system_prompt: str, keep_message_history: bool = True) -> None:
        self.messages = [{"role": "system", "content": system_prompt}]
        self.client = OpenAI()
        self.keep_message_history = keep_message_history

    def invoke(self, state: State) -> State:
        self.messages.append({"role": "user", "content": state.model_dump_json()})
        completion = openai.beta.chat.completions.parse(
            model="gpt-4o-2024-08-06",
            messages=self.messages,
            response_format=State,
        )
        state = completion.choices[0].message.parsed
        if self.keep_message_history:
            self.messages.append({"role": "assistant", "content": state.model_dump_json()})
        return state