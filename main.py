#import logging
from radon.complexity import cc_visit
from radon.metrics import mi_visit
import tkinter as tk
from tkinter import filedialog
import ast
import difflib
from ollama import chat
from ollama import ChatResponse
import ollama

def code_reader():
    root = tk.Tk()
    root.withdraw()

    file_path = filedialog.askopenfilename(
        title="Select a file to open",
        filetypes=(("Python files", "*.py"), ("All files", "*.*"))
    )
    if not file_path:
        return None
    with open(file_path,"r",encoding="utf-8") as file:
        return file.read()

def code_checker(code):
    try:
        ast.parse(code)
        return (True, None)
    except SyntaxError as e:
        #logging.exception("ERROR:Code has invalid syntax.")
        return (False, f"line {e.lineno}:{e.msg}")

def analyze(code):
    complexity_block = cc_visit(code)
    for block in complexity_block:
        print(f"Name: {block.name} | Complexity: {block.complexity}")

    maintainability_score = mi_visit(code,multi=True)
    print(f"Maintainability score: {maintainability_score:.2f}")
    report = {
        "complexity":{block.name:block.complexity for block in complexity_block},
        "maintainability":maintainability_score
        }
    return report

def optimize(code,report):
    user_prompt = 'You are an expert code optimizer. You need to read the code provided to you,' \
    ' analyze it completely and optimize it for better quality and maintainability in a production environment' \
    f' without altering the main functionality or breaking anything. Here is the code:{code}' \
    f' and here is the report:{report}. ONLY return the complete Python code, and give complete explanations of what was optimized and why by writing comments next to any line of code.'
    try:
        response:ChatResponse = chat(
            model='gemma4:e2b',
            messages=[
                {
                'role':'user',
                'content':user_prompt,
                },
            ],
        )
    except ollama.ResponseError as e:
        print(f"Error occurred in model usage:{e.status_code}")
        print(f"Error description:{e.error}")
        return None
    except ConnectionError as e2:
        print("Ollama not active. Try running Ollama first.")
        return None
    final_code = response['message']['content'].strip().splitlines()
    start = None
    end = None
    for i, line in enumerate(final_code):
        if line.startswith("```"):
            start = i
            break
    if start == None:
        return '\n'.join(final_code)
    for i, line in enumerate(final_code[start + 1:],start + 1):    
        if line.startswith("```"):
            end = i
            break
    if end == None:
        return '\n'.join(final_code[start + 1:])
    return '\n'.join(final_code[start + 1:end])

def show_code(old,new):
    diff = difflib.unified_diff(
        old.splitlines(),
        new.splitlines(),
        fromfile = 'old_code',
        tofile = 'new_code',
        lineterm=''
    )
    diff_output = '\n'.join(diff)
    if diff_output:
        print(diff_output)
    else:
        print("No difference in code.")    

def main():
    code = code_reader()
    if code is None:
        print("Action is cancelled")
        return None
    elif not code.strip():
        print("File is empty")
        return None
    ok1,error1 = code_checker(code)
    if not ok1:
        print("Your code has an error:",error1)
        return None
    report = analyze(code)   
    new_code = optimize(code,report)
    if new_code is None or not new_code.strip():
        print("No code returned by model.")
        return None
    ok2, error2 = code_checker(new_code)
    if not ok2:
        print("The model returned invalid code:",error2)
        return None
    show_code(code,new_code)

if __name__=="__main__":
    main()