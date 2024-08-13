class ToolBox: 
    def __init__(self) -> None:
        self.tools_dict = {}

    def store(self, tools):
        """
        Stores the literal name and docstring of each tool in the list. 

        Parameters: 
        tools (list): List of the function objects to store 

        Returns: 
        dict: A dictionary with key being the name of the tool and value being the description.
        """ 

        for tool in tools:
            self.tools_dict[tool.__name__] = tool.__doc__ 
        return self.tools_dict
    
    def tools(self): 
        """
        Returns the dictionary created in store a text string. 

        Returns: 
        str: Dictionary of stored function and their docsstrings as a string
        """
        tool_str = ""
        for name, doc in self.tools_dict.items(): 
            tool_str += f"{name}: \"{doc}\"\n"
        return tool_str.strip()

