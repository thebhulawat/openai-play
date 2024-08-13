import openai
import json


class OpenAIModel: 
    def __init__(self, model, system_prompt, temperature) -> None:
        self.client = openai.Client()
        self.model = model 
        self.temperature = temperature
        self.messages = [{"role": "system", "content": system_prompt.strip()}]

    def generate_text(self, prompt): 
        self.messages.append({"role": "user", "content": prompt.strip()})

        response = self.client.chat.completions.create(
            model= self.model, 
            messages=self.messages
        )
        response_content = response.choices[0].message.content
        cleaned_content = response_content.strip().removeprefix('```json').removesuffix('```').strip()

        response = json.loads(cleaned_content)
        return response