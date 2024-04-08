# Starter Llama-index with Retrieval Augmented Generation and Postgres/PGVector with Gradio UI

## About this lab

The intent of the code in this directory is to provide a basic introductory example of using the Llama-index library with Postgres and PGvector with a basic gradio web UI. 
This is not the easiest or best way to build a RAG agent with llama-index as there are tools such as create-llama available that easily create full stack agents in a more mature structure, but those approaches divide code across a more complex directory structure, making it more difficult to gain an understanding of the code. 
This project organizes the code in a much simpler structure intended to help gain an understanding of how the code works. Additional projects will be added to the parent repository to demonstrate additional and more mature use cases to deliver llama-index based agents.

The code in this directory is largely based on the llama-index documentation at [https://docs.llamaindex.ai/en/stable/examples/vector_stores/postgres](https://docs.llamaindex.ai/en/stable/examples/vector_stores/postgres). That being said, many of the commands used in that document did not work for me exactly so I have made some modifications. Also the code used in this lab includes a gradio web gui, which is not used in the llama-index documentation referenced. 

One of the advantages of using a container as a development environment is that anyone can load the same root container I am using and get the same exact environment. If you follow this approach you should be able to execute the same commands used in this document without issue. 

I am using the standard ubuntu:20.04 container on dockerhub. For example if you are using docker, you could load this container using the command `docker run -it ubuntu:20.04`.

## Instructions

I have only tested with and provide instructions for Ubuntu. Implementing this for other OS's may require adjustment/adaptation. I am using a Docker/OCI container using the standard ubuntu image hosted on docker hub. To follow this tutorial you do not need to use a container, there may be minimal differences if you install Ubuntu in a different way, but nothing that I think would cause any significant issues.

The ubuntu container I am using is a very minimal installation with almost nothing pre-installed. It defaults to the root user and does not include sudo, accordingly you will not see sudo used in the commands in this document. In many ubuntu installations you may need to use sudo for some of these commands. 

Using the root user for a container is not a recommendation or best practice, I am using it because its the default for the standard ubuntu container and I only use it in a temporary isolated environment for learning. I will post subsequent labs that provide further instruction on better methods for production and long-lived deployments . 

### Prepare Ubuntu Environment
I am using the Visual Studio Code IDE dev container plugin to access my container, which automatically installs anything needed for me to use VSCode as my text editor. If you prefer to use a different text editor, please install it. In this lab, you will be prompted to use a text editor and are free to choose your preferred text editor, explicit instructions for text editor selection or installation are not provided. 

```
apt update 
apt install -y curl git python3 pip virtualenv libpq-dev python3-dev
# Install node.js 20.x per https://deb.nodesource.com/
# node is not needed for this lab, but will be for some of the other labs in this repo
apt-get update && apt-get install -y ca-certificates curl gnupg
curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg
NODE_MAJOR=20
echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_$NODE_MAJOR.x nodistro main" | tee /etc/apt/sources.list.d/nodesource.list
apt-get update && apt-get install nodejs -y
```

### Prepare Postgres environment

Postgres is open source and can be installed freely. The following commands will install, launch and configure a postgres instance in your environment. It updates the default "postgres" user account with the password "password". You can use this value or modify the password if desired.

```
# install postgres
export LC_ALL=C
apt update
apt install -y postgresql-common
## The following command may require an interactive response
/usr/share/postgresql-common/pgdg/apt.postgresql.org.sh
## The following command may require an interactive response
apt install -y postgresql-15-pgvector
# launch and configure postgres
## update the postgres configuration to allow passwordless local authentication for the default "postgres" user
sed -i '/local\s\+all\s\+postgres\s\+peer/s/peer/trust/' /etc/postgresql/15/main/pg_hba.conf
service postgresql start
psql -U postgres -c "ALTER USER postgres PASSWORD 'password';"
## update the postgres configuration to use md5 local authentication for the default "postgres" user
sed -i '/local\s\+all\s\+postgres\s\+trust/s/trust/md5/' /etc/postgresql/15/main/pg_hba.conf
## create a PGPASSWORD environmental variable to enable db login without manually entering the password each time
export PGPASSWORD='password'
## Create a database named "vector_db" to be used for the vector store
psql -U postgres -c "CREATE DATABASE vector_db;"
```

### Clone this repository
```
git clone https://github.com/nkuhn-vmw/GenAI-for-TAS-Samples.git
cd GenAI-for-TAS-Samples/llama-index/starter_rag_postgres
```

### Recommended: create a virtual environment for python
```
virtualenv myenv
source myenv/bin/activate
```

### Install required python library components
```
pip install llama-index-vector-stores-postgres llama-index openai psycopg2 gradio
```

### Setup Reference Data for retrieval augmented generation
When you launch the python code you will create in this lab, it will automatically ingest any compatible file(s) in the /data subdirectory (GenAI-for-TAS-Samples/llama-index/starter_rag_postgres/data). 

This lab is not using image-capable or mixed-mode models, but can abstract text from most common document formats such as .txt, doc/docx, pdf etc.

You can place files you want to use for retrieval augmented generation in the ./data folder, or you can enter the following optional command to use the sample "Paul Graham Essay" provided by llama-index. 

```
wget 'https://raw.githubusercontent.com/run-llama/llama_index/main/docs/docs/examples/data/paul_graham/paul_graham_essay.txt' -O 'data/paul_graham_essay.txt'
```

### Enter your OpenAI API Key
Modify the following command using your own OpenAI Key and enter the command.
```
export OPENAI_API_KEY="your_openai_key"
```

### Prepare code file

Using your preferred text editor, create a file in this directory (GenAI-for-TAS-Samples/llama-index/starter_rag_postgres/) named `web.py`

The following code block includes the code you will need to enter in the web.py file, HOWEVER please read the inline instructions within the following code block and modify the code following the instructions as the code will not work for you if you cut and paste it directly without making the required modifications.

In the following code block, lines beginning with a single "#" are commented out commands provided for your reference. Lines beginning with 2 or more hashtags are instructions.

```
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
```

### Execute the code
Now that the code file is prepared, you can execute the file with python to run it with the following command:
```
python3 web.py
```

After you execute the code, you should see output similar to the following:
```
(myenv) root@llamabot:~/GenAI-for-TAS-Samples/llama-index/starter_rag_postgres# python3 web.py 
Document ID: 702aa78b-5266-4045-bca1-f2e8ecf3fdb1
Parsing nodes: 100%|█████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 10.46it/s]
Generating embeddings: 100%|███████████████████████████████████████████████████████████████| 22/22 [00:00<00:00, 26.66it/s]
Running on local URL:  http://0.0.0.0:7860
```
Observe that the final line of the output above shows that the server is running on `http://0.0.0.0:7860` which is effectively the same as `localhost` or `127.0.0.1`. At this point you should be able to access the chatbot web interface from your browser, just replace the `0.0.0.0` in the url with the word localhost like this: `http://localhost:7860`. In my case it is using port 7860, in your environment it may or may not use the same port number, so make sure to verify the port number shown in the output on your terminal to access the interface.

## Ask a question
Now you have prepared your environment and can ask a question that will use retrieval augmented generation. 

If you used your own data files to populate the knowledge base, try to ask some questions about information in the data files you provided to verify that the chatbot can now answer questions based on this data. 

If you used the example Paul Graham Essay as your data source, here are a couple sample questions you can ask to showcase how the chatbot is able to leverage this data source in its responses:

```
# Example Paul Graham Essay questions:
1. "What did the author do?"
2. "What happened in the mid 1980s?"
3. "Who does Paul Graham think of with the word schtick"
```