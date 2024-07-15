# Importing the necessary libraries
from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit

import logging
import os

from utils import *
from credentials import *
from input_handling import * 


# Ensure the log directory exists
log_dir = 'logs'
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, 'app.log')

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# File handler
file_handler = logging.FileHandler(log_file)
file_handler.setLevel(logging.INFO)

# Formatter for the log messages
formatter = logging.Formatter('%(asctime)s [%(levelname)s] - %(message)s')
file_handler.setFormatter(formatter)

# Add the file handler to the logger
logger.addHandler(file_handler)

# Console handler for debugging
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# Initialize Flask app
app = Flask(__name__, template_folder='../frontend/templates')

# Initialize SocketIO for real-time communication
socketio = SocketIO(app, debug=True, cors_allowed_origins='*', logger=True, engineio_logger=True)

@app.route('/', methods=['GET'])
def index():
    logger.info('Rendering index page')
    return render_template('index.html')

@socketio.on('extract_input')
def handle_run_code(data):
    logger.info('Received extract_input event with data: %s', data)
    code = handle_input(data['code'])
    error = handle_input(data['error'])
    model = data.get('model')
    
    if not code or not error:
        emit('result', {'output': 'Both code and error must be provided.'})
        return

    logger.info('Creating agent and task for the provided code and error')

    # Create agents and tasks for handling the code and error
    web_search_agent, code_fixing_agent, web_search_task, code_fixing_task = create_agents_and_tasks(code, error, model)
    
    # Create a crew to manage the tasks
    my_crew = create_crew(web_search_agent, code_fixing_agent, web_search_task, code_fixing_task)
    
    logger.info('Running the crew to handle the task')
    my_crew.kickoff()

    # Read the result from the output file
    with open('outputs/fixed_code.txt', 'r') as file:
        result = file.read()

    # Emit the result back to the client
    emit('result', {'output': result})

if __name__ == '__main__':
    logger.info('Starting Flask app with SocketIO')
    socketio.run(app, debug=True)
