from flask import Flask, request, jsonify
import os

# If script.py has imports or initial setups, they need to be included here
# Assuming script.py has a function named `chain` that you want to invoke
from script import chain  # This assumes that `chain.invoke(question)` is your AI processing function

app = Flask(__name__)

@app.route('/invoke', methods=['POST'])
def invoke_model():
    content = request.json
    question = content.get('question', '')
    try:
        response = chain.invoke(question)
        return jsonify({"response": response}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  # Adjust the host and port as needed