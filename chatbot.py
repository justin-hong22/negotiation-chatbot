import os
import openai
from dotenv import load_dotenv # type: ignore
from flask import Flask, request, jsonify, send_from_directory # type: ignore
import numpy as np
import math

#Setting up interaction between the HTML and Python
app = Flask(__name__)

#Embed the document chunks and relevant question here
def createEmbedding(text):
    response = openai.Embedding.create(
        input = text,
        model = "text-embedding-ada-002"
    )
    return response['data'][0]['embedding']

#Splitting up inputted document into smaller chunks of chunk_size words
def splitDocument(document, chunk_size = 2000):
    chunks = []
    words = document.split()
    for i in range(0, len(words), chunk_size):
        chunk = ' '.join(words[i : i + chunk_size])
        chunks.append(chunk)
    return chunks

def caluclateCosineSimilarity(v1, v2):
    dot_product = sum(a * b for a, b in zip(v1, v2))
    magnitudeA = math.sqrt(sum(a * a for a in v1))
    magnitudeB = math.sqrt(sum(b * b for b in v2))
    if magnitudeA == 0 or magnitudeB == 0:
        return 0
    return dot_product / (magnitudeA * magnitudeB)

#Find the relevant info and return the top_n results
def findSimilarChunk(questionEmbedding, docEmbeddings, top_n = 5):
    similarities = [caluclateCosineSimilarity(questionEmbedding, docEmbedding) for docEmbedding in docEmbeddings]
    similarities = np.array(similarities)
    topIndexes = similarities.argsort()[-top_n:][::-1]
    return topIndexes, similarities[topIndexes]

@app.route('/askChatGPT', methods=['POST'])
def askChatGPT():
    #Getting the question from JS file
    question = request.json.get('question')

    #Getting the most relevant info out of document here
    questionEmbedding = createEmbedding(question)
    top_indices, top_similarities = findSimilarChunk(questionEmbedding, chunkEmbeddings)
    text = "\n\n".join([chunks[i] for i in top_indices])

    #Generate the answer here
    response = openai.ChatCompletion.create(
            model = "gpt-3.5-turbo",
            messages = [
                {"role" : "system", "content" : f"You are answering questions based on the following text: {text}. Prioritize using this text to answer the question."},
                {"role": "user", "content": question}
            ],
            max_tokens = 512
        )

    answer = response.choices[0].message['content'].strip()
    return jsonify({"response" : answer})

@app.route('/')
def home():
    return app.send_static_file('index.html')

#########################################################
######### BELOW IS CALLED WHEN OPENING THE PAGE #########
#########################################################

#Getting the OpenAI API key without revealing what it is
load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

#Reading in and chunking the document here as soon as the website is accessed
documentText = ""
fileFolder = "documents"
for file in os.listdir(fileFolder):
    if file.endswith(".txt"):
        with open(os.path.join(fileFolder, file), 'r', encoding = 'latin-1') as f:
            documentText += f.read()

chunks = splitDocument(documentText)
chunkEmbeddings = [createEmbedding(chunk) for chunk in chunks]

#For testing locally only
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)