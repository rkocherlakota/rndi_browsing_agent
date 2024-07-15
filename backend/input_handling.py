import os

def handle_input(input_data):
    if os.path.isfile(input_data):
        with open(input_data, 'r') as file:
            content = file.read()
    else:
        content = input_data
    return content
