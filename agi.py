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

def openai_inference(prompt: str): 
     while True:
        try:
            # Use chat completion API
            response = "NOTHING"
            messages = [{"role": "system", "content": prompt}]
            response = openai.chat.completions.create(
                model="gpt-4o",
                messages=messages,
                n=1,
                stop=None,
            )
            return response.choices[0].message.content.strip()
        except openai.RateLimitError:
            print(
                "   *** The OpenAI API rate limit has been exceeded. Waiting 10 seconds and trying again. ***"
            )
            time.sleep(10)  # Wait 10 seconds and try again
        except openai.APIError:
            print(
                "   *** OpenAI API error occured. Waiting 10 seconds and trying again. ***"
            )
            time.sleep(10)  # Wait 10 seconds and try again
        finally:
            pass
            # print(f"Inference Response: {response}")

def expound_task(main_objective: str, current_task: str): 
    print(f"***Expounding based on task: {current_task}*** {current_task}")
    prompt = (f"You are an AI who performs one task based on the following objective: {main_objective}"
              f"Your task: {current_task}\n Response:")
    
    response = openai_inference(prompt)
    new_tasks = response.split("\n") if "\n" in response else [response]
    print(f"Expounded Tasks: {new_tasks}")
    return [{"task_name": task_name} for task_name in new_tasks]

# generate a bunch of tasks based on the main objective and the current task
def generate_tasks(MainObjective: str, TaskExpansion: str):
    prompt=(f"You are an AI who creates tasks based on the following MAIN OBJECTIVE: {MainObjective}\n"
            f"Create tasks pertaining directly to your previous research here:\n"
            f"{TaskExpansion}\nResponse:")
    response = openai_inference(prompt)
    new_tasks = response.split("\n") if "\n" in response else [response]
    task_list = [{"task_name": task_name} for task_name in new_tasks]
    new_tasks_list = []
    for task_item in task_list:
        # print(task_item)
        task_description = task_item.get("task_name")
        if task_description:
            # print(task_description)
            task_parts = task_description.strip().split(".", 1)
            # print(task_parts)
            if len(task_parts) == 2:
                new_task = task_parts[1].strip()
                new_tasks_list.append(new_task)

    return new_tasks_list

q = expound_task(main_objective, initial_task)

expounded_initial_task = dump_task(q)

tasks = generate_tasks(main_objective, expounded_initial_task)

task_counter = 0 
for task in tasks: 
    print(f"### {task} ###")
    e = expound_task(main_objective, task)
    print(dump_task(e))


