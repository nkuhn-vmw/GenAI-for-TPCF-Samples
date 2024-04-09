import streamlit as st
from langchain.llms import OpenAI
from streamlit_chat import message
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.embeddings import LocalAIEmbeddings
from langchain.vectorstores.pgvector import PGVector
from langchain.chat_models import ChatOpenAI
from langchain.prompts.prompt import PromptTemplate
from langchain.chains import ConversationalRetrievalChain
from langchain.docstore.document import Document
import psycopg2
import os
import pathlib
import httpx
import asyncio
from concurrent.futures import Future
from threading import Thread

from langchain.document_loaders.csv_loader import CSVLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.document_loaders import PyPDFLoader
from langchain.document_loaders import TextLoader

from cfenv import AppEnv

env = AppEnv()
pg = env.get_service(label='postgres')
llm = env.get_service(label='genai-service')
chunk_size = 500
chunk_overlap = 50

database_name = pg.credentials['db']
username = pg.credentials['user']
password = pg.credentials['password']
db_host = pg.credentials['hosts'][0]
db_port = pg.credentials['port']
conn = psycopg2.connect(database=database_name, user=username, password=password, host=db_host, port=db_port)
cur = conn.cursor()

#install pgvector
cur.execute("CREATE EXTENSION IF NOT EXISTS vector")
conn.commit()

connection_string = PGVector.connection_string_from_db_params(
     driver="psycopg2",
     host=db_host,
     port=int(db_port),
     database=database_name,
     user=username,
     password=password,
)

collection_name = "test1"

api_key = llm.credentials['api_key']
api_base = llm.credentials['api_base']

cwd = os.getcwd()

if 'history' not in st.session_state:
    st.session_state['history'] = []

if 'generated' not in st.session_state:
    st.session_state['generated'] = ["Hello ! Ask me anything!"]
if 'past' not in st.session_state:
    st.session_state['past'] = ["Hey ! 👋"]

def get_file_extension(uploaded_file):
    file_extension =  os.path.splitext(uploaded_file)[1].lower()
    return file_extension

def save_uploadedfile(uploadedfile):
     with open(os.path.join(cwd, uploadedfile.name), "wb") as f:
        f.write(uploadedfile.getbuffer())
     return uploadedfile.name

#This function will go through pdf and extract and return list of page texts.
def read_and_textify(file):
    text_splitter = RecursiveCharacterTextSplitter(
            chunk_size = 2000,
            chunk_overlap  = 100,
            length_function = len,
    )
    tmp_file_path = save_uploadedfile(file)
    file_extension = get_file_extension(tmp_file_path)
    if file_extension == ".csv":
        loader = CSVLoader(file_path=tmp_file_path, encoding="utf-8",csv_args={
            'delimiter': ',',})
        data = loader.load()
    elif file_extension == ".pdf":
        loader = PyPDFLoader(file_path=tmp_file_path)  
        data = loader.load_and_split(text_splitter)
    elif file_extension == ".txt":
        loader = TextLoader(file_path=tmp_file_path, encoding="utf-8")
        data = loader.load_and_split(text_splitter)
    return data

async def create_embeddings_async(documents):
    async with httpx.AsyncClient() as client:
        class AsyncOpenAIEmbeddings(OpenAIEmbeddings):
            async def _embed(self, text: str, *, engine: str):
                response = await client.post(
                    f"{self.openai_api_base}/v1/embeddings",
                    headers={"Authorization": f"Bearer {self.openai_api_key}"},
                    json={
                        "input": text,
                        "engine": engine,
                    },
                )
                response.raise_for_status()
                return response.json()["data"][0]["embedding"]

        embeddings = AsyncOpenAIEmbeddings(model="text-embedding-ada-002", openai_api_key=api_key, openai_api_base=api_base)
        PGVector.from_documents(documents, embeddings, 
                             collection_name=collection_name,
                             connection_string=connection_string)

def run_async(func, future, args):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    if args is None:
        result = loop.run_until_complete(func())
    else:
        result = loop.run_until_complete(func(args))
    future.set_result(result)

def create_embeddings(documents):
    future = Future()
    Thread(target=run_async, args=(create_embeddings_async, future, documents)).start()
    return future.result()
  
st.write("---")

st.title('Tanzu GPT: ChatBot with pgvector embeddings ')

#file uploader
uploaded_file = st.file_uploader("Upload document", type=["txt"])
upload_state = st.text_area("Upload State", "", key="upload_state")

def upload():
    if uploaded_file is None:
        st.session_state["upload_state"] = "Upload a file first!"
    else:
        documents = read_and_textify(uploaded_file)
        create_embeddings(documents)
        st.session_state["upload_state"] = uploaded_file.name + " loaded.."

st.button("Upload file", on_click=upload)

async def create_retriever_async():
    async with httpx.AsyncClient() as client:
        class AsyncOpenAIEmbeddings(OpenAIEmbeddings):
            async def _embed(self, text: str, *, engine: str):
                response = await client.post(
                    f"{self.openai_api_base}/v1/embeddings",
                    headers={"Authorization": f"Bearer {self.openai_api_key}"},
                    json={
                        "input": text,
                        "engine": engine,
                    },
                )
                response.raise_for_status()
                return response.json()["data"][0]["embedding"]

        embeddings = AsyncOpenAIEmbeddings(model="text-embedding-ada-002", openai_api_key=api_key, openai_api_base=api_base)
        vStore = PGVector(
            collection_name=collection_name,
            connection_string=connection_string,
            embedding_function=embeddings,
        )
        retriever = vStore.as_retriever()
        retriever.search_kwargs = {'k':2}
        return retriever

        embeddings = AsyncOpenAIEmbeddings(model="text-embedding-ada-002", openai_api_key=api_key, openai_api_base=api_base)
        vStore = PGVector(
            collection_name=collection_name,
            connection_string=connection_string,
            embedding_function=embeddings,
        )
        retriever = vStore.as_retriever()
        retriever.search_kwargs = {'k':2}
        return retriever

def create_retriever():
    future = Future()
    Thread(target=run_async, args=(create_retriever_async, future, None)).start()
    return future.result()

retriever = create_retriever()

#initiate model
llm = ChatOpenAI(model_name="gpt-3.5-turbo", openai_api_key=api_key, openai_api_base=api_base, streaming=True)

qa_template = """
    Conversational TAS Bot
    context: {context}
    =========
    question: {question}
    ======
    """
qa_prompt = PromptTemplate(template=qa_template, input_variables=["context","question" ])
response_container = st.container()
container = st.container()

chain = ConversationalRetrievalChain.from_llm(llm=llm,
    retriever=retriever, verbose=True, return_source_documents=True, max_tokens_limit=4097, combine_docs_chain_kwargs={'prompt': qa_prompt})

with container:
  with st.form(key='my_form', clear_on_submit=True):
      user_q = st.text_area("Enter your questions here")
      submit_button = st.form_submit_button(label='Send')

  if submit_button and user_q:
      chain_input = {"question": user_q, "chat_history": st.session_state["history"]}
      result = chain(chain_input)
      st.session_state["history"].append((user_q, result["answer"]))
      st.session_state['past'].append(user_q)
      st.session_state['generated'].append(result["answer"])

with response_container:
  for i in range(len(st.session_state['generated'])):
      message(st.session_state["past"][i], is_user=True, key=str(i) + '_user', avatar_style="big-smile")
      message(st.session_state["generated"][i], key=str(i), avatar_style="thumbs")