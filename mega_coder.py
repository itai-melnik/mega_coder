"""
This is a script which creates and runs python code
"""
import os
import subprocess
import time
import numpy as np
from google import genai
from dotenv import load_dotenv
from colorama import Fore, Style, init
from tqdm import tqdm
from gitingest import ingest
from mss import mss
from rapidocr_onnxruntime import RapidOCR
from openai import OpenAI
from PIL import Image
from code_detector import is_code




GENERATED_CODE_FILE_NAME = "generated_code_gemini.py"

SYSTEM_INSTRUCTION_DEFAULT = (
    "You are an expert Python developer that generates production-ready code. "
    "Follow these requirements strictly:\n\n"
    "CODE STRUCTURE:\n"
    "- Output ONLY Python code, no explanatory text or markdown\n"
    "- Add a comprehensive module docstring at the top\n"
    "- Use type hints for all functions (PEP 484)\n"
    "- Keep lines under 100 characters (PEP 8)\n\n"
    "QUALITY & SAFETY:\n"
    "- Add proper error handling with try-except blocks where appropriate\n"
    "- Validate all inputs and handle edge cases\n"
    "- Use meaningful, descriptive variable and function names\n"
    "- Add docstrings for all functions (parameters, returns, raises)\n"
    "- Avoid hardcoded values; use constants or configuration\n"
    "- Follow security best practices (no SQL injection, XSS, etc.)\n"
    "- Implement defensive programming principles\n\n"
    "TESTING & VERIFICATION:\n"
    "- Add comprehensive assert statements to verify correctness\n"
    "- Include test cases that cover normal and edge cases\n"
    "- Test for boundary conditions and invalid inputs\n\n"
    "DOCUMENTATION:\n"
    "- Add clear, concise comments for complex logic\n"
    "- Explain 'why' rather than 'what' in comments\n"
    "- Document assumptions and limitations\n\n"
    "If asked to fix code, analyze the issue thoroughly and return corrected code."
)


SYSTEM_INSTRUCTION_OPTIMIZE = (
    "You are an expert Python optimization specialist. "
    "Follow these requirements strictly:\n\n"
    "OPTIMIZATION GOALS:\n"
    "- Output ONLY optimized Python code, no explanatory text\n"
    "- Improve time complexity where possible (O(n²) → O(n log n) → O(n))\n"
    "- Reduce space complexity and memory usage\n"
    "- Use efficient data structures (sets, dicts, deques where appropriate)\n"
    "- Implement caching/memoization for repeated calculations\n"
    "- Minimize redundant operations and loops\n"
    "- Use list comprehensions and generators where beneficial\n"
    "- Leverage built-in functions and standard library\n\n"
    "CODE QUALITY:\n"
    "- Maintain all type hints and docstrings from original code\n"
    "- Keep lines under 100 characters (PEP 8)\n"
    "- Preserve all functionality and error handling\n"
    "- Do NOT remove asserts or test cases\n"
    "- Maintain the module docstring\n"
    "- Keep code readable; avoid over-optimization that harms clarity\n\n"
    "PERFORMANCE:\n"
    "- Profile-worthy optimizations only (no micro-optimizations)\n"
    "- Consider algorithmic improvements first\n"
    "- Use appropriate algorithms for the problem scale\n"
    "- Add comments explaining optimization techniques used"
)

SYSTEM_INSTRUCTION_FIX_GITHUB_REPOSITORY = (
    "You are an expert code reviewer and software architect. "
    "Analyze the provided GitHub repository and respond based on the user's request.\n\n"
    "OUTPUT FORMAT:\n"
    "- Provide a clear, structured explanation\n"
    "- Use markdown formatting for readability\n"
    "- Include code examples where relevant\n\n"
    "ANALYSIS APPROACH:\n"
    "- Identify issues, bugs, or areas for improvement\n"
    "- Explain the root cause of problems\n"
    "- Suggest specific, actionable fixes\n"
    "- Consider architecture, design patterns, and best practices\n"
    "- Address security vulnerabilities if present\n"
    "- Comment on code quality and maintainability\n"
    "- Suggest refactoring opportunities\n\n"
    "Be thorough, precise, and provide production-ready recommendations."
) 


load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")
gemini_client = genai.Client(api_key=gemini_api_key)


def generate_code(description, system_prompt=SYSTEM_INSTRUCTION_DEFAULT):
    """
    This function generates code based on the description
    """
    print(Fore.CYAN + "🤖 Generating code with Gemini AI...")
  
    response = gemini_client.models.generate_content(
        model="gemini-2.5-flash-lite",
        config=genai.types.GenerateContentConfig(
            system_instruction=system_prompt,
            response_mime_type="text/plain",
        ),
        contents=description
        
    )


     #write the code to a file
    clean_code = response.text.replace("```python", "").replace("```", "").strip()
    with open(GENERATED_CODE_FILE_NAME, "w", encoding="utf-8") as f:
        f.write(clean_code + '\n')  # Ensure exactly one final newline for pylint

    print(Fore.GREEN + "✓ Code generated successfully!")
    return clean_code


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


def check_lint_errors(file_path):
    """
    This function checks lint errors in the code file using flake8
    Returns the lint errors if any, otherwise returns None
    """
    print(Fore.CYAN + "🔍 Checking code with flake8...")
    result = subprocess.run(
        ["flake8", file_path, "--max-line-length=100"],
        capture_output=True,
        text=True,
        check=False)
    if result.returncode != 0:
        # return the lint errors
        print(Fore.YELLOW + "⚠ Lint issues found")
        return str(result.stdout)

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
                #generate new code with error context
                error_info = f"\nError Output:\n{result.stderr}\n\nStandard Output:\n{result.stdout}" if result.stderr or result.stdout else ""
                code = generate_code(f"Fix the following code: {code}{error_info}", SYSTEM_INSTRUCTION_DEFAULT)
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
    lint_errors = check_lint_errors(GENERATED_CODE_FILE_NAME)
    if lint_errors is not None:
        print(Fore.YELLOW + f"\n⚠ Lint issues detected. Attempting to fix (max {max_lint_attempts} attempts)...")
        with tqdm(total=max_lint_attempts, desc="Fixing lint issues", unit="attempt",
                  bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt}') as pbar:
            count = 0
            while lint_errors is not None and count < max_lint_attempts:
                count += 1
                pbar.set_description(f"Lint fix attempt {count}/{max_lint_attempts}")
                optimized_code = generate_code(f"Fix the following lint errors in the code: {lint_errors}\n\nCode:\n{optimized_code}", SYSTEM_INSTRUCTION_DEFAULT)
                lint_errors = check_lint_errors(GENERATED_CODE_FILE_NAME)
                pbar.update(1)

    if lint_errors is not None:
        print(Fore.YELLOW + "\n⚠ There are still lint errors/warnings.")
        return None

    print(Fore.GREEN + "\n✓ Amazing! No lint errors/warnings.")
    print(Fore.MAGENTA + "\n" + "="*50)
    print(Fore.GREEN + "🎉 Program Development Complete!")
    print(Fore.MAGENTA + "="*50 + "\n")

    return optimized_code



def analyze_github_repository(repository_url):
    """
    This function analyzes a github repository based on the description
    """
    print(Fore.CYAN + 'Tell me what you want me to fix/change/explain in that repository')
    description = input(Fore.WHITE + "Description: ")

    summary, tree, content = ingest(repository_url)

    MAX_CONTENT_LENGTH = 100000 

    if len(content) > MAX_CONTENT_LENGTH:
        print(Fore.YELLOW + f"⚠ Content truncated ({len(content)} → {MAX_CONTENT_LENGTH} chars)")
        content = content[:MAX_CONTENT_LENGTH] + "\n\n[... content truncated ...]"

    print(Fore.CYAN + "🔄 Analyzing repository with Gemini...")
    with tqdm(total=1, desc="Waiting for response", bar_format='{desc}', ncols=50):
        result = gemini_client.models.generate_content(
            model="gemini-2.5-pro",
            config=genai.types.GenerateContentConfig(
                system_instruction=SYSTEM_INSTRUCTION_FIX_GITHUB_REPOSITORY,
                response_mime_type="text/plain",
                max_output_tokens=1024,  # Limit output for faster response
            ),
            contents=f"Summary: {summary}\nTree: {tree}\nContent: {content}\nDescription: {description}"
        )

    print(Fore.GREEN + "✓ Analysis complete!\n")
    
    # Check if result has text content
    if result and result.text:
        print(Fore.GREEN + result.text)
    else:
        print(Fore.RED + "✗ No response received from Gemini. The model may have been blocked or returned empty content.")
        if hasattr(result, 'prompt_feedback'):
            print(Fore.YELLOW + f"Feedback: {result.prompt_feedback}")

    return 




def give_coding_tips():
    """
    This function gives coding tips based on screenshot of user's screen.
    Captures screen every second, uses OCR to extract text, detects code,
    and sends it to GPT-5-nano for analysis and tips.
    """
    print(Fore.CYAN + "Perfect. Show me your screen and I will be giving you tips on how to improve the code I see")
    print(Fore.YELLOW + "\n📸 Starting screen capture (Press Ctrl+C to stop)...")
    
    # Initialize OpenAI client
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        print(Fore.RED + "✗ Error: OPENAI_API_KEY not found in environment variables")
        return
    
    openai_client = OpenAI(api_key=openai_api_key)
    
    # Initialize RapidOCR
    ocr_engine = RapidOCR()
    
    # Store previous OCR text for comparison
    previous_text = ""
    
    print(Fore.GREEN + "✓ Ready! Monitoring your screen for code...\n")
    
    try:
        with mss() as sct:
            # Get the primary monitor
            monitor = sct.monitors[1]

                    
            # Define a region that excludes edges 
            # This captures the center 70% of the screen
            margin_horizontal = int(monitor['width'] * 0.18)  # 18% margin each side
            margin_vertical = int(monitor['height'] * 0.10)   # 10% margin top/bottom

            capture_region = {
                'left': monitor['left'] + margin_horizontal,
                'top': monitor['top'] + margin_vertical,
                'width': monitor['width'] - (2 * margin_horizontal),
                'height': monitor['height'] - (2 * margin_vertical),
            }

            
            while True:
                try:
                    # Capture screenshot
                    screenshot = sct.grab(capture_region)
                    
                    # Convert screenshot to format suitable for OCR
                    # mss returns a ScreenShot object, convert to PIL Image format
                    img = Image.frombytes('RGB', screenshot.size, screenshot.rgb)
                    img_array = np.array(img)
 
                    # Perform OCR
                    result, _ = ocr_engine(img_array)
                    
                    # Extract text from OCR result
                    if result:
                        # RapidOCR returns list of [bbox, text, confidence]
                        current_text = '\n'.join([item[1] for item in result])
                    else:
                        current_text = ""


                    
                    # Check if text is different from previous frame and not empty
                    if current_text and current_text != previous_text:
                        # Check if the text appears to be code
                        if is_code(current_text):
                            print(Fore.CYAN + "\n" + "="*60)
                            print(Fore.CYAN + "🔍 Code detected! Analyzing...")
                            print(Fore.CYAN + "="*60 + "\n")
                            
                            try:
                                # Send to GPT-5-nano for analysis
                                response = openai_client.responses.create(
                                    model="gpt-5-nano",
                                    input=f"Analyze the following code and provide tips to improve it. Keep your response concise (max 3-4 key tips):\n\n{current_text}",
                                    max_output_tokens=512  # Limit output for faster response
                                )
                                
                                # Print the response
                                print(Fore.GREEN + "💡 Coding Tips:")
                                print(Fore.WHITE + response.output_text)
                                print(Fore.CYAN + "\n" + "="*60 + "\n")
                                
                            except Exception as api_error:
                                print(Fore.RED + f"✗ API Error: {api_error}")
                        
                        # Update previous text
                        previous_text = current_text
                    
                except Exception as capture_error:
                    print(Fore.RED + f"✗ Capture Error: {capture_error}")
                
                # Wait 1 second before next capture
                time.sleep(1)
                
    except KeyboardInterrupt:
        print(Fore.YELLOW + "\n\n⚠ Screen monitoring stopped by user")
        print(Fore.GREEN + "✓ Goodbye!")
    except Exception as e:
        print(Fore.RED + f"\n✗ Unexpected error: {e}")
           

    

   

  

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
        print(Fore.CYAN + '\n💭 Give me the full url of a public github repository:')
        repository_url = input(Fore.WHITE + "Repository URL: ")
        analyze_github_repository(repository_url)
    elif choice == "3":
        give_coding_tips()
    else:
        print(Fore.RED + "\n✗ Invalid choice. Please try again.")




if __name__ == "__main__":
    main()
