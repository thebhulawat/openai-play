import openai
import time 




main_objective = "Become a machine learning expert"
initial_task = "Learn about tensors"

print ("***Objective***")
print(f"{main_objective}")

def dump_task(task): 
    d = ""
    for tasklet in task: 
        d += f"\n {tasklet.get('task_name', '')}"
    d.strip()
    return d

def open_ai_inference(prompt: str): 
    messages = [{"role": "user", "content": prompt}]
    response = openai.chat.completions.create(model="gpt-4o", messages=messages)
    return response.choices[0].message.content.strip()

def expound_task(main_objective: str, current_task: str): 
    print(f"***Expounding based on task: {current_task}*** {current_task}")
    prompt = (f"You are an AI who performs one task based on the following objective: {main_objective}"
              f"Your task: {current_task}\n Response:")
    
    response = open_ai_inference(prompt)
    new_tasks = response.split("\n") if "\n" in response else [response]
    print(f"Expounded Tasks: {new_tasks}")
    return [{"task_name": task_name} for task_name in new_tasks]


q = expound_task(main_objective, initial_task)

expounded_initial_task = dump_task(q)

tasks = GenerateTasks(main_objective, expounded_initial_task)

task_counter = 0 
for task in tasks: 
    print(f"### {task} ###")
    e = expound_task(main_objective, task)
    print(dump_task(e))


