from flask import Flask, render_template, request
from dotenv import load_dotenv
import os
from langchain_text_splitters import RecursiveCharacterTextSplitter, HTMLHeaderTextSplitter
from langchain_community.vectorstores import Milvus
from langchain_community.embeddings import OctoAIEmbeddings
from langchain_community.llms.octoai_endpoint import OctoAIEndpoint
from langchain.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
import json

app = Flask(__name__)

# Load environment variables
load_dotenv()
OCTOAI_API_TOKEN = os.environ["OCTOAI_API_TOKEN"]

# Initialize components
html_splitter = HTMLHeaderTextSplitter(headers_to_split_on=[("h1", "Header 1"), ("h2", "Header 2"), ("h3", "Header 3"), ("h4", "Header 4"), ("div", "Divider")])
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1024, chunk_overlap=128)
llm = OctoAIEndpoint(model="llama-2-13b-chat-fp16", max_tokens=1024, presence_penalty=0, temperature=0.1, top_p=0.9)
embeddings = OctoAIEmbeddings(endpoint_url="https://text.octoai.run/v1/embeddings")
prompt = ChatPromptTemplate.from_template(template="""You are an assistant that gives an accessibility score. \
                                          Give number formatted as "Accessibility Score: (score)" and then use three \
                                          sentences maximum and keep the answer concise. Use specific examples from the website and style
                                          the output in html. Question: {question} Context: {context} Answer:""")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    website_name = request.form['website_name']
    html_header_splits = html_splitter.split_text_from_url(website_name)
    splits = text_splitter.split_documents(html_header_splits)
    vector_store = Milvus.from_documents(
        splits,
        embedding=embeddings,
        connection_args={"host": "localhost", "port": 19530},
        collection_name="starwars"
    )
    retriever = vector_store.as_retriever()
    chain = ({"context": retriever, "question": RunnablePassthrough()} | prompt | llm | StrOutputParser())

    out = str(chain.invoke("What is my score and why?"))  # Process the data

    # Extract accessibility score
    accessibility_score = extract_accessibility_score(out)

    # Render template with accessibility score and chart
    return render_template('result.html', output=out, accessibility_score=accessibility_score)

def extract_accessibility_score(output):
    # Extract the accessibility score from the output
    # You need to implement your own logic to extract the score from the output
    # For example, using regular expressions or string manipulation
    accessibility_score = 90  # Replace this with your actual score extraction logic
    return accessibility_score

if __name__ == '__main__':
    app.run(debug=True)
