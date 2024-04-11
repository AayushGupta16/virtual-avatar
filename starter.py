import os
from dotenv import load_dotenv
from llama_index.core import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    StorageContext,
    load_index_from_storage,
)
from llama_index.core.tools import QueryEngineTool, ToolMetadata
from llama_index.agent.openai import OpenAIAgent
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.openai import OpenAI
from llama_index.core import Settings
import nest_asyncio
import requests

CHUNK_SIZE = 1024
url = "https://api.elevenlabs.io/v1/text-to-speech/<voice-id>"
headers = {
    "Accept": "audio/mpeg",
    "Content-Type": "application/json",
    "xi-api-key": "<xi-api-key>",
}
OPENAI_API_KEY: os.getenv("OPENAI_API_TOKEN")
nest_asyncio.apply()

# Load environment variables
load_dotenv()

# Check if storage already exists
PERSIST_DIR = "./storage"
if not os.path.exists(PERSIST_DIR):
    # Load the documents and create the index
    documents = SimpleDirectoryReader("data/txt").load_data()
    index = VectorStoreIndex.from_documents(documents)
    # Store it for later
    index.storage_context.persist(persist_dir=PERSIST_DIR)
else:
    # Load the existing index
    storage_context = StorageContext.from_defaults(persist_dir=PERSIST_DIR)
    index = load_index_from_storage(storage_context)

# Settings for LlamaIndex
Settings.chunk_size = 512
Settings.chunk_overlap = 64
Settings.llm = OpenAI(model="gpt-4-0125-preview")
Settings.embed_model = OpenAIEmbedding(model="text-embedding-3-small")

# Setup Query Engine Tool for the index
query_engine_tool = QueryEngineTool(
    query_engine=index.as_query_engine(),
    metadata=ToolMetadata(
        name="vector_index",
        description="Provides information about Thirus policies and opinions. "
        "Use a detailed plain text question as input to the tool.",
    ),
)

# Create an OpenAIAgent with the query engine tool
agent = OpenAIAgent.from_tools(
    tools=[query_engine_tool],
    llm_kwargs={
        "temperature": 0,
        "max_tokens": 500,
        "model_name": "gpt-4-0125-preview",
        "openai_api_key": os.getenv("OPENAI_API_TOKEN"),
    },
    verbose=True,  # Enables verbose output to see the agent's internal process
)

# # Chatbot loop
# while True:
#     user_input = input("User: ")
#     if user_input.lower() == "exit":
#         break
#     prompt_template = (
#     "User: You are Baltimore Mayoral Candidate Thiruvendran Tignarajah, also known as Thiru."
#     "There are provided tools which you can use to access your policies and views"
#     "Please answer from the perspective of Thiru."
#     "When the user says You, Your, etc they mean Thiru or Thiru's so please respond as if they are asking about Thiru"
#     "Example:"
#     "User: What are your views about ..."
#     "You: Thiru's views about this are ... "
#     "User:"
# )
#     # Use the processed input for the chatbot response
#     response = agent.chat(prompt_template+user_input)
#     print(f"Chatbot: {response}")


def convert_text_to_speech(text):
    data = {
        "text": text,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {"stability": 0.5, "similarity_boost": 0.5},
    }
    response = requests.post(url, json=data, headers=headers)
    audio_content = b""
    for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
        if chunk:
            audio_content += chunk
    return audio_content


def process_message(user_input):
    prompt_template = (
        "Instructions- You are Baltimore Mayoral Candidate Thiruvendran Tignarajah, also known as Thiru."
        "There are provided tools which you can use to access your policies and views, please be as detailed as possible and substitute words like you/your for Thiru and Thirus"
        "When the user says You, Your, etc they mean Thiru or Thiru's so please respond as if they are asking about Thiru"
        "Example:"
        "User: What are your views about the inner harbor"
        'Calling function: vector_index with args: {"input":"Thirus views on the Baltimore Inner Harbor"}'
        "You: Thiru's views about this are ... "
        "The information you are given is from Thiru's past writings and interviews. "
        "If there is a question that Thiru might not have spoken about or is not included in your dataset,"
        "please tell the user that the chatbot is based on Thiru's policies and that they should reach out to Thirus campaign directly"
        "Through the email teamthiru@votethiru.com"
        "\n\n\n\n\nUser:"
    )
    
    text_msg = str(agent.chat(prompt_template + user_input))
    audio_msg = convert_text_to_speech(text_msg)
    
    return text_msg, audio_msg
