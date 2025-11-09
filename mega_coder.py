"""
This is a script which creates and runs python code
"""
import os
import subprocess
import time
from google import genai
from dotenv import load_dotenv



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

     #write the code to a file
    with open(GENERATED_CODE_FILE_NAME, "w") as f:
        f.write(response.text.replace("```python", "").replace("```", ""))

    return response.text.replace("```python", "").replace("```", "")


def run_code_docker(file_name) -> tuple[int, float]:
    """
    This function runs the code using docker
    """
    #TODO: add error handling for the docker run
    #TODO: add timing for the docker run

    
   

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
        print("Docker run timed out")
        return None
    except subprocess.CalledProcessError as e:
        print(f"Docker run failed: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

    return result, end_time - start_time


def develop_program(description):
    """
    This function develops a python program based on the description
    
    """
    code = generate_code(description, SYSTEM_INSTRUCTION_DEFAULT)
    #run the code using docker
    result, execution_time = run_code_docker(GENERATED_CODE_FILE_NAME)


     # if errors in generated code, call gemini to fix the code and then run the code again up to 5 times
    count = 0
    while result.returncode != 0 and count < 5:
        count += 1
        print(f"Error in code. Attempting to fix... {count}/5")
        #generate new code
        code = generate_code(f"Fix the following code: {code}", SYSTEM_INSTRUCTION_DEFAULT)
        #run the code again
        result, execution_time = run_code_docker(GENERATED_CODE_FILE_NAME)

    if result.returncode != 0:
        print("Sorry master, I have failed you. I can't create this program without issues.")
        return None
    else: 
        #optimize the code
        generate_code(f"Optimize the following code: {code}", SYSTEM_INSTRUCTION_OPTIMIZE)
        #run the optimized code
        result, optimized_execution_time = run_code_docker(GENERATED_CODE_FILE_NAME)
        print(f"Code runnign time optimized! It now runs in {optimized_execution_time} milliseconds, while it was {execution_time} milliseconds")
        

    return 



def main():
    """
    This is the main function which creates and runs python code
    """

    print("I'm Mega Coder. What would you like me to do today?\n1. Develop a python program.\n2. Fix/change something in a Github repository.\n3. Look at my screen and give me realtime coding tips.")
    choice = input("Enter your choice: ")
    if choice == "1":
        #ask the user for the program they want to develop
        print('Describe me which python program you want me to develop:')
        #await the description of the user and then send to gemini to generate the code
        description = input("Enter the description: ")
        develop_program(description)
        
    elif choice == "2":
        print("not implemented yet")
    elif choice == "3":
        print("not implemented yet")
    else:
        print("Invalid choice. Please try again.")




if __name__ == "__main__":
    load_dotenv()
    main()