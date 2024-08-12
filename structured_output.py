from openai import OpenAI 
from pydantic import BaseModel

client = OpenAI() 

class CalendarEvent(BaseModel): 
    name: str
    date: str 
    participants: list[str]

calendar_event_schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "date": {"type": "string"},
        "participants": {
            "type": "array",
            "items": {"type": "string"}
        }
    },
    "required": ["name", "date", "participants"],
    "additionalProperties": False,
}

# method 1 
completions = client.beta.chat.completions.parse(
    model="gpt-4o-2024-08-06", 
    messages=[
        {"role": "system", "content": "Extract the event Inforomation"}, 
        {"role": "user", "content": "Alice and Bob are going to a science fair on Friday"}
    ],
    response_format=CalendarEvent
)

# method 2
# completions = client.beta.chat.completions.parse(
#     model="gpt-4o-2024-08-06", 
#     messages=[
#         {"role": "system", "content": "Extract the event Inforomation"}, 
#         {"role": "user", "content": "Alice and Bob are going to a science fair on Friday"}
#     ],
#     response_format={"type": "json_schema", "json_schema": {"strict": True, "schema": calendar_event_schema, "name": "calendar_event"}}
# )

# -- response -- #
# ParsedChatCompletionMessage[CalendarEvent](content='{"name":"Science Fair","date":"Friday","participants":["Alice","Bob"]}', refusal=None, role='assistant', function_call=None, tool_calls=[], parsed=CalendarEvent(name='Science Fair', date='Friday', participants=['Alice', 'Bob']))

#print(completions.choices[0].message)
print(completions.choices[0].message.parsed)

event: CalendarEvent = completions.choices[0].message.parsed
print(event.date)
print(event.participants)
print(event.name)

