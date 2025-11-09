"""
This is a script which creates and runs python code
"""
import os
import subprocess
import time
import random
from google import genai
from dotenv import load_dotenv
from colorama import Fore, Style, init
from tqdm import tqdm



GENERATED_CODE_FILE_NAME = "generated-code-gemini.py"

SYSTEM_INSTRUCTION_DEFAULT = "You are a helpful assistant that " \
+ "generates python code based on the description. " \
+ "You only output the code, no other text. " \
+ "add minimalcomments or descriptions but enough so that AI can understand the code and the logic. " \
+ "Your output will be copied to a python file" \
+ "Add Asserts to the generated code that check that the logic is correct. " \
+ "If asked to fix the code, fix it and return the correct code. "


SYSTEM_INSTRUCTION_OPTIMIZE = "You are a helpful assistant that " \
+ "optimizes the input code based on the description. " \
+ "You only output the code, no other text." \
+ "add minimal comments or descriptions but enough so that AI can understand the code and the logic." \
+ "Your output will be copied to a python file" \
+ "do not remove the asserts or the test cases from the code. "

def generate_code(description, system_prompt=SYSTEM_INSTRUCTION_DEFAULT):
    """
    This function generates code based on the description
    """
    print(Fore.CYAN + "🤖 Generating code with Gemini AI...")
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    client = genai.Client(api_key=gemini_api_key)
    #TODO: add roles and instructions to the gemini model and checks.
    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        config=genai.types.GenerateContentConfig(
            system_instruction=system_prompt,
            response_mime_type="text/plain",
        ),
        contents=description
        
    )

    response_text = response.text
    #TODO: add random errors just for testing (remove this later)
    if random.random() < 0.5:
        response_text = response_text + "\nx = 1 / 0  # Testing error handling"


     #write the code to a file
    with open(GENERATED_CODE_FILE_NAME, "w") as f:
        f.write(response_text.replace("```python", "").replace("```", ""))

    print(Fore.GREEN + "✓ Code generated successfully!")
    return response_text.replace("```python", "").replace("```", "")


def run_code_docker(file_name) -> tuple[int, float]:
    """
    This function runs the code using docker
    """
    #TODO: add error handling for the docker run
    #TODO: add timing for the docker run

    print(Fore.CYAN + "🐳 Running code in Docker container...")
    try:
        start_time = time.time()
        result = subprocess.run(
            ["docker", "run", "--rm", "-v", f"{os.getcwd()}:/app", 
            "python:3.11", "python", f"/app/{file_name}"],
            capture_output=True,
            text=True,
            timeout=30,
            check=False)
        end_time = time.time()
    except subprocess.TimeoutExpired:
        print(Fore.RED + "✗ Docker run timed out")
        return None
    except subprocess.CalledProcessError as e:
        print(Fore.RED + f"✗ Docker run failed: {e}")
        return None
    except Exception as e:
        print(Fore.RED + f"✗ An unexpected error occurred: {e}")
        return None

    if result.returncode == 0:
        print(Fore.GREEN + "✓ Code executed successfully!")
    else:
        print(Fore.RED + f"✗ Code execution failed with return code {result.returncode}")
    
    return result, end_time - start_time


def check_lint_errors(code):
    """
    This function fixes lint errors in the code
    Returns the lint errors if any, otherwise returns None
    """
    print(Fore.CYAN + "🔍 Checking code with pylint...")
    result = subprocess.run(
        ["pylint", code],
        capture_output=True,
        text=True,
        check=False)
    if result.returncode != 0:
        #return the lint errors
        print(Fore.YELLOW + "⚠ Lint issues found")
        return str(result.stderr)

    print(Fore.GREEN + "✓ No lint errors!")
    return None



def develop_program(description):
    """
    This function develops a python program based on the description
    
    """
    print(Fore.MAGENTA + "\n" + "="*50)
    print(Fore.MAGENTA + "🚀 Starting Program Development Pipeline")
    print(Fore.MAGENTA + "="*50 + "\n")
    
    code = generate_code(description, SYSTEM_INSTRUCTION_DEFAULT)
    #run the code using docker
    result, execution_time = run_code_docker(GENERATED_CODE_FILE_NAME)

    


     # if errors in generated code, call gemini to fix the code and then run the code again up to 5 times
    max_fix_attempts = 5
    if result.returncode != 0:
        print(Fore.YELLOW + f"\n⚠ Code has errors. Attempting to fix (max {max_fix_attempts} attempts)...")
        with tqdm(total=max_fix_attempts, desc="Fixing errors", unit="attempt", 
                  bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt}') as pbar:
            count = 0
            while result.returncode != 0 and count < max_fix_attempts:
                count += 1
                pbar.set_description(f"Fix attempt {count}/{max_fix_attempts}")
                #generate new code
                code = generate_code(f"Fix the following code: {code}", SYSTEM_INSTRUCTION_DEFAULT)
                #run the code again
                result, execution_time = run_code_docker(GENERATED_CODE_FILE_NAME)
                pbar.update(1)

    if result.returncode != 0:
        print(Fore.RED + "\n✗ Sorry master, I have failed you. I can't create this program without issues.")
        return None
    
    print(Fore.GREEN + "\n✓ Code is working!")
    
    #optimize the code
    print(Fore.MAGENTA + "\n" + "-"*50)
    print(Fore.MAGENTA + "⚡ Optimization Phase")
    print(Fore.MAGENTA + "-"*50)
    optimized_code = generate_code(f"Optimize the following code: {code}", SYSTEM_INSTRUCTION_OPTIMIZE)
    #run the optimized code
    result, optimized_execution_time = run_code_docker(GENERATED_CODE_FILE_NAME)
    
    # Calculate improvement
    improvement = ((execution_time - optimized_execution_time) / execution_time) * 100
    print(Fore.MAGENTA + f"\n⚡ Performance: {execution_time:.4f}s → {optimized_execution_time:.4f}s " + 
          f"({improvement:+.1f}% change)")
        

    #lint check the code using pylint up to 3 times
    print(Fore.MAGENTA + "\n" + "-"*50)
    print(Fore.MAGENTA + "🔍 Lint Check Phase")
    print(Fore.MAGENTA + "-"*50)
    
    max_lint_attempts = 3
    lint_errors = check_lint_errors(f"{optimized_code}")
    if lint_errors is not None:
        print(Fore.YELLOW + f"\n⚠ Lint issues detected. Attempting to fix (max {max_lint_attempts} attempts)...")
        with tqdm(total=max_lint_attempts, desc="Fixing lint issues", unit="attempt",
                  bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt}') as pbar:
            count = 0
            while lint_errors is not None and count < max_lint_attempts:
                count += 1
                pbar.set_description(f"Lint fix attempt {count}/{max_lint_attempts}")
                code = generate_code(f"Fix the following lint errors in the code: {lint_errors} + {optimized_code}", SYSTEM_INSTRUCTION_DEFAULT)
                lint_errors = check_lint_errors(f"{optimized_code}\n{code}")
                pbar.update(1)

    if lint_errors is not None:
        print(Fore.YELLOW + "\n⚠ There are still lint errors/warnings.")
        return None

    print(Fore.GREEN + "\n✓ Amazing! No lint errors/warnings.")
    print(Fore.MAGENTA + "\n" + "="*50)
    print(Fore.GREEN + "🎉 Program Development Complete!")
    print(Fore.MAGENTA + "="*50 + "\n")

    return code


def main():
    """
    This is the main function which creates and runs python code
    """
    # Initialize colorama for cross-platform colored output
    init(autoreset=True)
    
    print(Fore.CYAN + Style.BRIGHT + "\n" + "="*60)
    print(Fore.CYAN + Style.BRIGHT + "           🤖 MEGA CODER - AI Code Generator 🤖")
    print(Fore.CYAN + Style.BRIGHT + "="*60)
    print(Fore.WHITE + "\nWhat would you like me to do today?\n")
    print(Fore.GREEN + "  1. 💻 Develop a python program")
    print(Fore.YELLOW + "  2. 🔧 Fix/change something in a Github repository")
    print(Fore.MAGENTA + "  3. 👁️  Look at my screen and give me realtime coding tips")
    print(Fore.CYAN + "\n" + "-"*60)
    
    choice = input(Fore.WHITE + "Enter your choice (1-3): ")
    
    if choice == "1":
        #ask the user for the program they want to develop
        print(Fore.CYAN + '\n💭 Describe the python program you want me to develop:')
        #await the description of the user and then send to gemini to generate the code
        description = input(Fore.WHITE + "Description: ")
        develop_program(description)
        
    elif choice == "2":
        print(Fore.YELLOW + "\n⚠ Not implemented yet")
    elif choice == "3":
        print(Fore.YELLOW + "\n⚠ Not implemented yet")
    else:
        print(Fore.RED + "\n✗ Invalid choice. Please try again.")




if __name__ == "__main__":
    load_dotenv()
    main()