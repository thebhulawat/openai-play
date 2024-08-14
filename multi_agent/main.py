from agent.agent import Agent
from agent.orchestrator import Orchestrator
from prompt.prompt import planner_system_prompt, executor_system_prompt
from state.state import State, AgentState
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

if __name__ == "__main__":
    planner = Agent(planner_system_prompt)
    executor = Agent(executor_system_prompt, False)
    orchestrator = Orchestrator(planner, executor)

    initial_state = State(
        objective="Create a small blog post on Rust programming langauge",
        current_state=AgentState.PLAN,
        final_response=None,
        task_list=[],
        current_task=None
    )

    print(f"{Fore.CYAN}{'='*50}")
    print(f"{Fore.YELLOW}Starting Multi-Agent System")
    print(f"{Fore.YELLOW}Objective: {Fore.GREEN}{initial_state.objective}")
    print(f"{Fore.CYAN}{'='*50}\n")

    final_state = orchestrator.run(initial_state)
    print("Final State:")
    print(final_state.model_dump_json(indent=2))