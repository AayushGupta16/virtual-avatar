import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("OPENAI_API_TOKEN"),
)


# Read input data from text file
def read_input_data(file_path):
    with open(file_path, "r") as file:
        return file.read()


# Write GPT-4's response to a text file
def write_response_to_file(response, file_path):
    with open(file_path, "w") as file:
        file.write(response)


def main():
    # Get the path to the directory containing the data folder
    current_directory = os.path.dirname(os.path.abspath(__file__))
    data_directory = os.path.join(current_directory, "..", "data")

    # Read input data from text file
    input_data = read_input_data(
        os.path.join(data_directory, "JUFJ Questionnaire 2020.txt")
    )

    # Ask a question to GPT-4
    # question = "What are your top three priorities and specific proposals for how to achieve those priorities?"
    starting_line = "Hi! I hope you're having a great day. How can I assist you today?"
    question = input(starting_line + "\n" + "\n")
    prompt = (
        input_data
        + "\nQuestion: "
        + question
        + "\nInstruction: Respond from the perspective of a politician.\nAnswer:"
    )
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="gpt-4",
        max_tokens=500,
        temperature=1,
    )

    # Get GPT-4's response
    gpt4_response = chat_completion.choices[0].message.content

    # Write GPT-4's response to another text file
    write_response_to_file(gpt4_response, "gpt4_response.txt")
    
    print('\n' + gpt4_response)


if __name__ == "__main__":
    main()
