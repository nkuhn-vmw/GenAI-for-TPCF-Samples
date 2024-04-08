### - Optional Logging Configuration
## Logging is optional, uncomment the following lines if you want to enable logging
# import logging
# import sys
# logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
# logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))
###

### Import required libraries
from llama_index.core import SimpleDirectoryReader, StorageContext
from llama_index.core import VectorStoreIndex
from llama_index.vector_stores.postgres import PGVectorStore
import textwrap
import openai

### Initialize Model API Key
## You must have the environmental variable OPENAI_API_KEY set to the value of your OpenAI API Keya
## This command extracts your API key from the environmental variable for use by this code file
import os
openai.api_key = os.environ["OPENAI_API_KEY"]

### Load your documents
## This code creates a variable named documents which is populated with the documents in the /data folder
## This makes the documents available within the code's runtime environment so they can later be indexed

documents = SimpleDirectoryReader("./data").load_data()
print("Document ID:", documents[0].doc_id)

### Initialize database
## In an earlier step you created a database named "vector_db" which was done to ensure postgres installed correctly
## The following command will delete and recreate the "vector_db" database to ensure it is properly initialized
import psycopg2

connection_string = "postgresql://postgres:password@localhost:5432"
db_name = "vector_db"
conn = psycopg2.connect(connection_string)
conn.autocommit = True

with conn.cursor() as c:
    c.execute(f"DROP DATABASE IF EXISTS {db_name}")
    c.execute(f"CREATE DATABASE {db_name}")
###

### Initialize vector store
## The following code initializes a PGVectorStore named vector_store, and extracts the required paramaters from the connection string entered above
from sqlalchemy import make_url
url = make_url(connection_string)
vector_store = PGVectorStore.from_params(
    database=db_name,
    host=url.host,
    password=url.password,
    port=url.port,
    user=url.username,
    table_name="paul_graham_essay",
    embed_dim=1536,  # openai embedding dimension
)
###

### Ingest data, create embeddings and vector index
storage_context = StorageContext.from_defaults(vector_store=vector_store)
index = VectorStoreIndex.from_documents(
    documents, storage_context=storage_context, show_progress=True
)
###

### Gradio Web UI Configuration
## Import components required for gradio UI
import json
import gradio as gr
## The chatbot function is called by the gradio web interface to process responses
## The chatbox function does the following:
## 1. Recieves the user's question (input_text) when called by the gradio web UI when the user hits the submit button
## 2. Uses the vector store index to instantiate a query engine (The query engine is provided by llama-index)
## 3. Calls the query_engine.query method with the user's question (input_text) and saves the response in the "responce" variable.
## 3. (continued) The query_engine.query method does a search on the vector database which includes the data you provided in the /data folder. 
## 3. (continued) Next the method takes the information found from the search of your data, and it creates a prompt to send to the model (e.g. gpt-3.5 turbo) which includes the search data along with the users question
## 3. (continued) Next the prompt with the context from data is sent as an api call to the model, and the model returns a response in JSON format.
## 4. The JSON response from the model API is decoded
## 5. The decoded response is returned to the caller (the gradio web interface)
def chatbot(input_text):
    query_engine = index.as_query_engine()
    response = query_engine.query(input_text)
    print("Response:", response.response)
    try:
        json.loads(response.response)
    except json.JSONDecodeError as e:
        print("Invalid JSON:", e)
    return response.response
## The following code configures the Gradio web UI
## Observe that the first line of the function defines "fn=chatbot", which instructs the interface to call the chatbot function defined on the previous lines to handle requests
iface = gr.Interface(
    fn=chatbot,
    inputs=[
        gr.Textbox(lines=7, label="How may I help you?"),
    ],
    outputs="text",
    title="My-Starter-ChatBot",
)
## The following line starts the gradio web server which serves the web user interface
iface.launch(debug=True, server_name="0.0.0.0")
###