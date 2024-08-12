from typing import Any
import openai 
import re 
import httpx 
from dotenv import load_dotenv

load_dotenv()

class Bot: 
    def __init__(self, system_message = "") -> None:
        self.system_message = system_message
        self.messages = []
        if self.system_message: 
            self.messages.append({"role": "system", "content": system_message})
        
    def __call__(self, message, *args: Any, **kwds: Any) -> Any:
        self.messages.append({"role": "user", "content": message})
        result = self.execute()
        self.messages.append({"role": "assistant", "content": result})
        return result
    
    def execute(self): 
        response = openai.chat.completions.create(
            model="gpt-4", 
            messages=self.messages
        )
        return response.choices[0].message.content


prompt = """
You run in a loop of Thought, Action, PAUSE and Observation.
At the end of the loop you output an answer. 
Use Thought to describe the thought about the question you have been asked. 
Use Action to run one of the actions available to you - then return PAUSE.
Observation will be the result of running those actions. 

Your available actions are: 
calculate: 
e.g. calculate: (4*7/3)
Run a calculation and returns a nuber - uses Python so be sure to use floating syntax if necessary. 


wikipedia: 
e.g. wikipedia: Django 
Returns a summary be searching the wikipedia

simon_blog_search: 
e.g. simon_blog_search: Django 
Search Simon's blog for a search term 

Example session: 
Question: What is the capital of France? 
Thought: I should look up France on Wikipedia 
Action: wikipedia: France 
PAUSE 

You will be called again with this: 
Observation: France is a country. The capital is Paris. 

You then output: 
Answer: The capital of France is Paris
""".strip()

action_re = re.compile(r'^Action: (\w+): (.*)')

def wikipedia(q): 
    response = httpx.get("https://en.wikipedia.org/w/api.php", params={
        "action": "query", 
        "list": "search",
        "srsearch": q, 
        "format": "json"
    })
    return response.json()["query"]["search"][0]["snippet"]

def simon_blog_search(q):
    response = httpx.get("https://datasette.simonwillison.net/simonwillisonblog.json", params={
        "sql": """
        select
          blog_entry.title || ': ' || substr(html_strip_tags(blog_entry.body), 0, 1000) as text,
          blog_entry.created
        from
          blog_entry join blog_entry_fts on blog_entry.rowid = blog_entry_fts.rowid
        where
          blog_entry_fts match escape_fts(:q)
        order by
          blog_entry_fts.rank
        limit
          1
          """.strip(), 
          "_shape": "array", 
          "q": q,
          "timeout":10.0,
    })
    return response.json()[0]["text"]


def calculate(what): 
    return eval(what)

# def web_search(q): 
#     #client = Client(os.getenv("TAVILY_API_KEY"))
#     client = TavilyClient()
#     response = client.qna_search(q)
#     return response

tools = {
    "wikipedia": wikipedia,
    "calculate": calculate, 
    "simon_blog_search": simon_blog_search, 
    #"web_search": web_search
}
    
def query(question, max_turns = 10): 
    i = 0 
    bot = Bot(prompt)
    next_prompt = question
    while i < max_turns:
        i = i + 1 
        result = bot(next_prompt)
        print(result)
        actions = [action_re.match(line) for line in result.split('\n') if action_re.match(line)]
        if actions: 
            action, action_input = actions[0].groups() 
            if action not in tools: 
                raise Exception(f"Unknown action {action} with input {action_input}")
            print("--- Running Action {} {} ---".format(action, action_input))
            observation = tools[action](action_input)
            print("Observation: {}",observation)
            next_prompt = f"Observation: {observation}"
        else: 
            return result
        
print(query("what are simon's view on AI and programming"))



