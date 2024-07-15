# Browsing Agent

This application is designed to assist developers in resolving errors encountered while executing Python code. 
It leverages AI models and web search tools to research, gather information, and provide solutions for Python code errors.

## Frontend

The frontend folder contains files related to the user interface and client-side functionality.

### Structure

- **templates/**: Stores HTML templates.
  - **index.html**: HTML template for the main application page.
  - **style.css**: CSS stylesheet for styling the frontend.

## Backend

The backend folder contains files responsible for server-side logic, AI model configurations, and data processing.

### Structure

- **model.py**: Defines AI models and their configurations.
- **credentials.py**: Manages API keys and credentials.
- **input_handling.py**: Handles input data processing.
- **utils.py**: Contains utility functions and tools.
- **app.py**: Implements the Flask application and handles server-side logic.
- **main.py**: Entry point for running the backend application.

## Configuration

- **.env.example**: Example file for environment variables. Rename to `.env` and add your credentials.
- **.gitignore**: Specifies intentionally untracked files to ignore.
- **requirements.txt**: Lists all required Python packages for installing dependencies.

## Installation

To set up the application, follow these steps:

1. Clone the repository:

    ```bash
    git clone git@github.com:rkocherlakota/rndi_browser_agent.git
    ```

2. Navigate to the project directory:

    ```bash
    cd browsing_agent
    ```

3. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. Start the Flask application:

    ```bash
    python backend/app.py
    ```

2. Access the application through your browser at `http://localhost:5000`.

3. Enter the Python code snippet and the encountered error message in the provided input fields.

4. Select the AI model (Claude or GPT-3.5 Turbo) you want to use for error resolution.

5. Click on the "Submit" button to initiate the error resolution process.

6. Follow the instructions provided by the virtual assistants to identify and implement the appropriate fix for the error.

7. Once the process is complete, the corrected code will be displayed along with an explanation of the fix.

## Contributing

Contributions are welcome! If you have any suggestions, bug reports, or feature requests, please open an issue or submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.