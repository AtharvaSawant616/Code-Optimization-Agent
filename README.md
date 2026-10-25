# Code-Optimization-Agent
This is a privacy-first agent that checks code syntax, measures code quality using Radon, and uses a local LLM (Ollama) to provide more readable and maintainable code.
This agent runs locally on a model, and checks code syntax before and after the model runs. Currently, it accepts python code as input and outputs optimized python code. Expect updates in the future so that the agent accepts other languages of coding.

Design logic:
1. User selects a file of python code to upload to the agent.
2. AST (Abstract Syntax Tree) is used to parse the code and validate it's syntax. If it fails, then the line is reported and everything stops.
3. Radon is used to check the current code's maintainability and complexity.
4. Ollama to accept user input and create the optimized code based on the prompt.
5. Second validation of the model's output
6. Output is shown to the user

Setup and usage:
1. Python version, and pip install ollama radon (or a requirements.txt)
2. Install Ollama and run ollama pull gemma4:e2b
3. python main.py, then pick a file in the dialog
4. Add a note that the model name is one line in optimize() and can be swapped
5. Mention that the file picker uses tkinter, which needs a desktop environment

Future plans:
- Add a feature to accept coding of other languages
