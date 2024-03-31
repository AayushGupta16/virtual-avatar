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

# Load environment variables from .env file
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

query_engine = index.as_query_engine()

# Define a QueryEngineTool for the index
query_engine_tool = QueryEngineTool(
    query_engine=query_engine,
    metadata=ToolMetadata(
        name="vector_index",
        description="Useful for answering queries about the loaded documents",
    ),
)

# Define a custom prompt template
prompt_template = (
    "You are a helpful chatbot assistant who is here to answer questions about Baltimore Mayor Candidate Thiruvendran Tignarajah, also known as Thiru."
    "Use the provided tools to answer the user's questions.\n"
    "User: {input}\n"
    "Chatbot: "
)

# Create an OpenAIAgent with the query engine tool, custom prompt, and specified model
agent = OpenAIAgent.from_tools(
    [query_engine_tool],
    prompt=prompt_template,
    llm_kwargs={
        "temperature": 0.7,
        "max_tokens": 500,
        "model_name": "gpt-4-0125-preview",
        "openai_api_key": os.getenv("OPENAI_API_TOKEN"),
    },
)

# Chatbot loop
while True:
    user_input = input("User: ")
    if user_input.lower() == "exit":
        break
    response = agent.chat(user_input)
    print(f"Chatbot: {response}")

