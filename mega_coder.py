"""
This is a script which creates and runs python code
"""
import os
from google import genai
from dotenv import load_dotenv

def generate_code(description):
    """
    This function generates code based on the description
    """
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    client = genai.Client(api_key=gemini_api_key)
    #TODO: add roles and instructions to the gemini model and checks.
    #TODO: add system prompt to the gemini model.
    return client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=description,
    )



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
        code = generate_code(description)
        print(code.text)
    elif choice == "2":
        print("not implemented yet")
    elif choice == "3":
        print("not implemented yet")
    else:
        print("Invalid choice. Please try again.")




if __name__ == "__main__":
    load_dotenv()
    main()