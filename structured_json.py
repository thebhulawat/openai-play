from openai import OpenAI 
import json

client = OpenAI() 

def get_delivery_date(order_id: str) -> str:
    if order_id == "1": 
        return "13th Aug, 2024"
    elif order_id == "2": 
        return "14th Aug, 2024"
    else: 
        return "15th Aug, 2024"

# chat_completions = client.chat.completions.create(
#     model="gpt-4o-2024-08-06", 
#     messages=[{"role":"system", "content":"your name is ram"},{"role": "user", "content": "what is your name?"}])

# print(chat_completions.choices[0])

tools = [
    {
        "type": "function", 
        "function": {
            "name": "get_delivery_date", 
            "description": "Get the delviery date for a cusotmer's order. Call this whenever you need to get the delivery date for a customer's order",
            "parameters": {
                "type": "object", 
                "properties": {
                "order_id": {
                    "type": "string", 
                    "description": "order id of the customer's order",
                    }
                },
            "required": ["order_id"],
            "additionalProperties": False
            }
        }
    }
]

messages = [
    {
        "role": "system", 
        "content": "You are customer support executive. Answer al lthe queries from customer apporpirately",
    },
    {
        "role": "user", 
        "content": "When will my order be delivered?"
    }
]

# -- response -- #
# Choice(finish_reason='stop', index=0, logprobs=None, message=ChatCompletionMessage(content='Could you please provide me with your order ID so I can check the delivery date for you?', refusal=None, role='assistant', function_call=None, tool_calls=None))

messages.append({"role": "assistant", "content": "Could you please provide me with your order ID? This will allow me to check the delivery date for you"})
messages.append({"role": "user", "content": "my order id is 1"})

response = client.chat.completions.create(
    model="gpt-4o-2024-08-06", 
    tools=tools, 
    messages=messages
)



# -- response -- #
# Choice(finish_reason='tool_calls', index=0, logprobs=None, message=ChatCompletionMessage(content=None, refusal=None, role='assistant', function_call=None, tool_calls=[ChatCompletionMessageToolCall(id='call_SV5n5Dgx2jzC16dheGfq6meF', function=Function(arguments='{"order_id":"2"}', name='get_delivery_date'), type='function')]))

#print(response.choices[0])

tool_call = response.choices[0].message.tool_calls[0]

args = tool_call.function.arguments

args_dict = json.loads(args)

order_id = args_dict["order_id"]

delivery_date = get_delivery_date(order_id)

#print(delivery_date)

function_call_result_message = {
    "role": "tool", 
    "content": json.dumps({
        "order_id": order_id, 
        "delivery_id": delivery_date
    }), 
    "tool_call_id": tool_call.id
}

messages.append(response.choices[0].message)
messages.append(function_call_result_message)

print(messages)

response = client.chat.completions.create(
    model="gpt-4o-2024-08-06", 
    tools=tools, 
    messages=messages
)

print(response.choices[0].message)