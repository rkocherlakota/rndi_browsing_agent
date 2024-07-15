# Importing the necessary libraries
from utils import *
from credentials import *
from input_handling import *

def main():

    code = """ 
ngkhyfrtykfhjnkiuygtfgcvgbhjkuygtfgvhjgyf
"""

    error = """ error """

    # Assuming the user chooses the model 'claude'
    model_choice = 'openai'

    # Create agents and tasks
    web_search_agent, code_fixing_agent, web_search_task, code_fixing_task = create_agents_and_tasks(
        code, error, model_choice
    )

    # Create crew
    my_crew = create_crew(
        web_search_agent, code_fixing_agent, web_search_task, code_fixing_task
    )

    # Execute crew tasks
    my_crew.kickoff()

if __name__ == "__main__":
    main()