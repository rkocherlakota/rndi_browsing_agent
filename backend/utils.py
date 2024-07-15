# Importing the necessary libraries
from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool

from credentials import *
from credentials import *
from model import *
from input_handling import *


# Define functions
def create_agents_and_tasks(code, error, model_choice):
    """
    Create agents and tasks for error resolution in Python code.
    
    Parameters:
    - code: str, the Python code that encountered an error.
    - error: str, the error message encountered.
    - model_choice: str, choice of model ('openai' or 'claude').
    
    Returns:
    - web_search_agent: Agent, the agent responsible for web research.
    - code_fixing_agent: Agent, the agent responsible for fixing the code.
    - web_search_task: Task, the task for web research.
    - code_fixing_task: Task, the task for code fixing.
    """
    
    # Select the model based on user input
    if model_choice == "openai":
        selected_model = openai_model
    elif model_choice == "claude":
        selected_model = claude_model
    else:
        raise ValueError("Invalid model choice. Please select 'openai' or 'claude'.")
    print("Selected model:", selected_model)

    # Define the SearchTool 
    search_tool = SerperDevTool()

    # Initialize the web search agent
    web_search_agent = Agent(
        role='Researcher',
        goal='Identify and resolve errors encountered while executing a code script.',
        backstory=(f"""
            You are a dedicated assistant assigned to find solutions for errors that occured while executing a code script. 
            Your task is to research and gather accurate information from reliable online sources to fix the error. 
            Follow the below instructions to achieve your goal.
            <instructions>
            1. Analyze the Error Message: Understand the meaning and implications of the error message.
            2. Comprehend the Code Context: Review the provided code to grasp its purpose and functionality. 
            Also check the programming language and framework used in the provided code so that you can have a look at the official documentations of those frameworks for resolving the errors.
            3. Research and Gather Solutions: Use the internet to find solutions for the error. 
            Consult official documentations related to the framework, to search for the error fix. 
            If you cannot find the valid fix in the official documentation, then check forums, Stack Overflow posts, Reddit, Quora, GeeksforGeeks, and other trustworthy sources where similar issues have been addressed.
            4. Evaluate and Compile Potential Fixes: Based on your research, compile appropriate solutions for the error. 
            Ensure that these solutions are reliable and have been verified by a resource.
            5. When a Perfect Fix is not found: If you can't find a direct or related solution, explain potential causes of the error and offer suggestions on how to fix it.
            6. Provide References for Further Exploration: Conclude your response by including links to the webpages where you found the fix for user's reference.
            The links should redirect the user to the webpages where the fix can be found, do not directly provide the website link.
            </instructions>

            <rules>
            1. Do not assume and do not hallucinate anything. If you do not know the answer to any question, just say that you do not know the answer politely.
            2. If you cannot find the exact fix for the error caused, strictly do not attempt to resolve the error by yourself; instead, focus on suggesting possibilities and guiding further exploration.
            3. Double-check before providing the links to the webpages whether they will redirect the user to the correct pages and ensure the pages are found and will not throw 'PAGE NOT FOUND ERROR'.
            </rules>

            The error you need to address is: {error}
            The code that encountered the error is: {code}

            Take a deep breath and think step by step then do the task.
            """
        ),
        verbose=True,
        llm=selected_model,
        function_calling_llm=selected_model,
        allow_delegation=False
    )

    # Initialize the code fixing agent
    code_fixing_agent = Agent(
        role='Python Developer',
        goal='Find a valid fix to resolve the error',
        backstory=(f"""
            You are a helpful assistant tasked with identifying and implementing a valid fix for the error among the various fixes collected by a previous researcher.
            Your goal is to find one valid fix for the error.
            Follow the below instructions to achieve your goal.
                   
            <instructions>
            1. Analyze the error message: Understand what the error message is indicating.
            2. Comprehend the Code Context: Review the provided code to understand its purpose and functionality.
            3. Evaluate Potential Fixes: Check all the fixes collected by the previous agent (web_search_agent) and determine a valid and appropriate fix for the error.
            4. Implement the Fix (if applicable): If a valid fix is found, integrate it into the provided code and return the complete code.
            Ensure that the integrated code resolves the error while maintaining the overall functionality and integrity of the original code.
            Also ensure to return the total corrected script, do not just return the corrected snippet.
            5. Explain the Fix (if applicable): After integrating the fix into the code snippet, provide a concise explanation of what caused the error and how the fix addresses the issue. 
            Demonstrate your understanding of the problem and the solution.
            6. When a Perfect Fix is not found: If no suitable fix is found among the suggestions, or if they:
                a. Don't directly address the error in your code.
                b. Introduce new problems,
            First let the user know that you did not find a perfect solution to resolve the error.
            Check if you found any documentation where similar issues have been discussed.
            If you have any suggestions, let the user know you are having suggestions on how to fix the error and then suggest possibilities and guide the user towards a solution to fix the error.
            Politely explain what might be causing the error and alternative approaches for troubleshooting and resolving the issue.
            Do not attempt to modify (integrate the suggestions) the code in this scenario.
            7. Reference for Further Exploration (if applicable): If a fix is implemented, provide a link to the webpage where you found the solution for user's reference.
            Double-check: The link should redirect the user to the correct and functional page.
            </instructions>
                   
            <rules>
            1. Do not assume and do not hallucinate anything.
            If you do not know the answer to any question, just say that you do not know the answer politely.
            But do not try to fix the error based on any assumptions.
            Remember, your answer to any question should always be based on a source not on assumptions or hallucinations.
            2. If you cannot find the exact fix for the error caused, strictly do not attempt to resolve the error by yourself.
            3. When a fix is integrated with the provided python script, you must return the total corrected script, rather than just returning the corrected snippet so the user can run the script directly without the need of making any changes manually.
            </rules>
                   
            The error encountered is: {error}
            The code that encountered the error is: {code}

            Take a deep breath and think step by step then do the task.
            """
        ),
        verbose=True,
        llm=selected_model,
        function_calling_llm=selected_model,
        allow_delegation=False
    )

    # Ensure output directories exist
    os.makedirs('outputs', exist_ok=True)

    # Define the web search task
    web_search_task = Task(
        description='Find the fixes for errors that occurred while executing a Python code',
        expected_output=(
            "A list of fixes to resolve the encountered error\n"
            "And the link to the webpage where you found the fix for user's reference."
        ),
        async_execution=False,
        agent=web_search_agent,
        tools=[search_tool],
        output_file='outputs/fixes.txt'
        # human_input=True
    )

    # Define the code fixing task
    code_fixing_task = Task(
        description='Find a valid fix to resolve the error',
        expected_output=(
            "A Python code which has been corrected and is free from all the errors.\n"
            "Concise explanation of what caused the error and how the fix addresses the issue.\n"
            "And the link to the webpage where you found the fix for user's reference."
        ),
        context=[web_search_task],
        async_execution=False,
        agent=code_fixing_agent,
        output_file='outputs/fixed_code.txt'
    )

    return web_search_agent, code_fixing_agent, web_search_task, code_fixing_task

def create_crew(web_search_agent, code_fixing_agent, web_search_task, code_fixing_task):
    """
    Create a Crew with the specified agents and tasks.
    
    Parameters:
    - web_search_agent: Agent, the agent responsible for web research.
    - code_fixing_agent: Agent, the agent responsible for fixing the code.
    - web_search_task: Task, the task for web research.
    - code_fixing_task: Task, the task for code fixing.
    
    Returns:
    - my_crew: Crew, the initialized crew with the agents and tasks.
    """
    
    # Initialize the Crew with the agents and tasks
    my_crew = Crew(
        agents=[web_search_agent, code_fixing_agent],
        tasks=[web_search_task, code_fixing_task],
        process=Process.sequential,
        full_output=True,
        memory=True,
        verbose=True,
        output_log_file=True
    )
    return my_crew
