def reverse_string(input_string): 
    """
    Reverse the given string 

    Parameters: 
    input_string(str): The string to be reversed. 

    Returns: 
    str: The reversed string 
    """
    reverse_string = input_string[:: -1]

    reverse_string = f"The reversed string is: {reverse_string}\n\n. Exectued using the reverse_string function"
    return reverse_string