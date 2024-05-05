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
import matplotlib.pyplot as plt
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
prompt = ChatPromptTemplate.from_template(template="""You are an AI assistant tasked with evaluating web accessibility.
                     Return a JSON object containing key accessibility metrics from the website.
                     Include metrics such as "text_contrast_ratio", "alt_text_usage", "keyboard_navigability",
                     and "ARIA_landmark_roles". Provide concise explanations for each metric based on specific
                     examples observed on the website. Ensure your response is structured for clarity and precision.
                     \
                     Question: {question} Context: {context} Answer:""")

@app.route('/')
def index():
    return render_template('index.html')

# @app.route('/process', methods=['POST'])
# def process():
#     website_name = request.form['website_name']
#     html_header_splits = html_splitter.split_text_from_url(website_name)
#     splits = text_splitter.split_documents(html_header_splits)
#     vector_store = Milvus.from_documents(
#     splits,
#         embedding=embeddings,
#         connection_args={"host": "localhost", "port": 19530},
#         collection_name="starwars"
#     )
#     retriever = vector_store.as_retriever()
#     chain = ({"context": retriever, "question": RunnablePassthrough()} | prompt | llm | StrOutputParser())
#
#
#     out = str(chain.invoke("What is my score and why?"))  # Process the data
#     return render_template('result.html', output=out)



def create_accessibility_chart(json_data):
    metrics = json.loads(json_data)
    labels = metrics.keys()
    values = metrics.values()

    plt.figure(figsize=(10, 5))
    plt.bar(labels, values, color=['blue', 'green', 'red', 'purple'])
    plt.xlabel('Accessibility Metric')
    plt.ylabel('Score')
    plt.title('Website Accessibility Evaluation')
    plt.ylim(0, 1)  # Assuming scores are between 0 and 1
    plt.savefig('/path/to/static/charts/accessibility_chart.png')  # Save the plot
    plt.close()
    return 'charts/accessibility_chart.png'

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
    chart_path = create_accessibility_chart(out)  # Create the chart and get the path
    return render_template('result.html', output=out, chart_path=chart_path)

if __name__ == '__main__':
    app.run(debug=True)
