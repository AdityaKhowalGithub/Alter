# %%
! pip install -q langchain-openai langchain langchain-text-splitters lxml octoai-sdk pymilvus
! playwright install  

# %%
! pip install -q langchain-openai langchain langchain-text-splitters lxml octoai-sdk pymilvus

# %%
!docker compose up -d

# %%
from dotenv import load_dotenv
import os

load_dotenv()
#OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
OCTOAI_API_TOKEN = os.environ["OCTOAI_API_TOKEN"]

# %%
from langchain_text_splitters import RecursiveCharacterTextSplitter, HTMLHeaderTextSplitter
url = "https://en.wikipedia.org/wiki/Star_Wars"

headers_to_split_on = [
    ("h1", "Header 1"),
    ("h2", "Header 2"),
    ("h3", "Header 3"),
    ("h4", "Header 4"),
    ("div", "Divider")
]

html_splitter = HTMLHeaderTextSplitter(headers_to_split_on=headers_to_split_on)

# for local file use html_splitter.split_text_from_file(<path_to_file>)
html_header_splits = html_splitter.split_text_from_url(url)

# %%
chunk_size = 1024
chunk_overlap = 128
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=chunk_size,
    chunk_overlap=chunk_overlap,
)

# Split
splits = text_splitter.split_documents(html_header_splits)

# %%
from langchain_community.vectorstores import Milvus

# %%
from langchain_community.embeddings import OctoAIEmbeddings
from langchain_community.llms.octoai_endpoint import OctoAIEndpoint
llm = OctoAIEndpoint(
        model="llama-2-13b-chat-fp16",
        max_tokens=1024,
        presence_penalty=0,
        temperature=0.1,
        top_p=0.9,
        
    )
embeddings = OctoAIEmbeddings(endpoint_url="https://text.octoai.run/v1/embeddings")

# %%
vector_store = Milvus.from_documents(
    splits,
    embedding=embeddings,
    connection_args={"host": "localhost", "port": 19530},
    collection_name="starwars"
)

# %%
retriever = vector_store.as_retriever()

# %%
from langchain.prompts import ChatPromptTemplate
template="""You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question. If you don't know the answer, just say that you don't know. Use three sentences maximum and keep the answer concise.
Question: {question} 
Context: {context} 
Answer:"""
prompt = ChatPromptTemplate.from_template(template)

# %%
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

# %%
chain.invoke("Who is Luke's Father?")

# %%
chain.invoke("what is most popular starwars movie?")

# %%



