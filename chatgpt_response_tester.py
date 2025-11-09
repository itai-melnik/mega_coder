import os
from openai import OpenAI
from dotenv import load_dotenv


def main():
    
    load_dotenv()
    openai_api_key = os.getenv("OPENAI_API_KEY")
    client = OpenAI(api_key=openai_api_key)
    print('waiting for response...')

    response = client.responses.create(
        model="gpt-5-nano",
        input="What is the capital of France?"
    )

    print(response.output_text)


if __name__ == "__main__":
    main()