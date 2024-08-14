from pydantic import BaseModel, Field
from enum import Enum
from typing import List, Optional


class AgentState(str, Enum): 
    IDLE = "idle"
    PLAN = "plan"
    EXECUTE_TASK = "execute_task"
    REVIEW_TASK = "review_task"
    COMPLETED = "completed"

class Task(BaseModel): 
    id: int
    description: str
    result: Optional[str]

class State(BaseModel): 
    objective: str
    final_response: Optional[str] 
    task_list: List[Task] 
    current_task: Optional[Task]
    current_state: AgentState 

    class Config: 
        use_enum_values = True



if __name__ == "__main__":
    # Initialize the state
    state = State(objective="Create a blog post about AI")

    # Add tasks
    state.task_list.append(Task(id=1, description="Research AI topics"))
    state.task_list.append(Task(id=2, description="Create outline"))
    state.task_list.append(Task(id=3, description="Write introduction"))

    # Update current state and task
    state.current_state = AgentState.PLAN
    state.current_task = state.task_list[0]

    # Print the current state
    print(state.model_dump_json(indent=2))