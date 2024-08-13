from toolbox.toolbox import ToolBox
from prompts.prompt import agent_system_prompt_template
from models.ollama_model import OllamaModel
from termcolor import colored 


class Agent: 
    def __init__(self, tools, model_service, model_name, stop = None) -> None:
        """
        Initialize the tool with a list of tools and a model. 

        Parameters: 
        tools (list): List of tool functions 
        model_service (class): the model service class with a generate_text method 
        model_name (str): The name of the model to use
        """
        self.tools = tools
        self.model_service = model_service
        self.model_name = model_name 
        self.stop = stop 

    def prepare_tools(self): 
        """
        Stores the tools in the toolbox and returns their description 

        Returns: 
        str: Description of the tools in the toolbox
        """
        toolbox = ToolBox() 
        toolbox.store(self.tools)
        tools_description = toolbox.tools()
        return tools_description
    
    def think(self, prompt):
        """
        Runs the generate_text method of the the model using the prompt template and description. 

        Parameters: 
        prompt (str): The user query to generate a response for. 

        Returns: 
        dict: The response from the model as a dictionary. 
        """

        tool_descriptions = self.prepare_tools() 
        agent_system_prompt = agent_system_prompt_template.format(tool_descriptions = tool_descriptions)
        if self.model_service == OllamaModel: 
            model_instance = self.model_service(
                model = self.model_name, 
                system_prompt = agent_system_prompt, 
                temperature = 0, 
                stop = self.stop
            )
        else: 
            model_instance = self.model_service(
                model = self.model_name, 
                system_prompt = agent_system_prompt,
                temperature = 0
            )
        
        agent_response_dict = model_instance.generate_text(prompt)
        return agent_response_dict
    
    def work(self, prompt): 
        agent_response_dict = self.think(prompt)
        tool_choice = agent_response_dict.get("tool_choice")
        tool_input = agent_response_dict.get("tool_input")

        for tool in self.tools:
            if tool.__name__ == tool_choice: 
                response = tool(tool_input)
                print(colored(response, 'cyan')), 
                return
            





    
 