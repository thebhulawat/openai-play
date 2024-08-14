# agent/orchestrator.py
from state.state import State, AgentState, Task
from agent.agent import Agent
from colorama import Fore, init
import textwrap

# Initialize colorama
init(autoreset=True)

class Orchestrator:
    def __init__(self, planner: Agent, executor: Agent):
        self.planner = planner
        self.executor = executor

    def run(self, initial_state: State) -> State:
        state = initial_state
        while state.current_state != AgentState.COMPLETED:
            if state.current_state == AgentState.PLAN:
                self._print_state(state, "Planner")
                state = self.planner.invoke(state)
                print(f"{Fore.MAGENTA}Planner has updated the state.")
            elif state.current_state == AgentState.EXECUTE_TASK:
                self._print_state(state, "Executor")
                state = self.executor.invoke(state)
                print(f"{Fore.MAGENTA}Executor has completed a task.")
                if state.current_state and state.current_task.result:
                    self._print_task_result(state.current_task)
            elif state.current_state == AgentState.REVIEW_TASK:
                self._print_state(state, "Planner")
                state = self.planner.invoke(state)
                print(f"{Fore.MAGENTA}Planner has reviewed the task.")
            else:
                raise ValueError(f"Unexpected state: {state.current_state}")
        
        self._print_final_response(state)
        return state
    
    def _print_state(self, state: State, agent_type: str):
        print(f"{Fore.CYAN}{'='*50}")
        print(f"{Fore.YELLOW}Current State: {Fore.GREEN}{state.current_state}")
        print(f"{Fore.YELLOW}Agent: {Fore.GREEN}{agent_type}")
        if state.current_task:
            print(f"{Fore.YELLOW}Current Task: {Fore.GREEN}{state.current_task.description}")
        print(f"{Fore.YELLOW}Task List:")
        for task in state.task_list:
            status = "✓" if task.result else " "
            print(f"{Fore.GREEN}  [{status}] {task.description}")
        print(f"{Fore.CYAN}{'='*50}")

    def _print_task_result(self, task: Task):
        print(f"{Fore.CYAN}{'='*50}")
        print(f"{Fore.YELLOW}Task Completed: {Fore.GREEN}{task.description}")
        print(f"{Fore.YELLOW}Result:")
        wrapped_result = textwrap.wrap(task.result, width=80)
        for line in wrapped_result:
            print(f"{Fore.WHITE}{line}")
        print(f"{Fore.CYAN}{'='*50}")

    def _print_final_response(self, state: State):
        print(f"\n{Fore.GREEN}{'='*50}")
        print(f"{Fore.GREEN}Objective Completed!")
        print(f"{Fore.GREEN}{'='*50}")
        print(f"{Fore.YELLOW}Final Response:")
        wrapped_response = textwrap.wrap(state.final_response, width=80)
        for line in wrapped_response:
            print(f"{Fore.WHITE}{line}")
        print(f"{Fore.GREEN}{'='*50}")