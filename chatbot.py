import os
import openai
from sklearn.metrics.pairwise import cosine_similarity # type: ignore
from dotenv import load_dotenv # type: ignore

#Getting the OpenAI API key without revealing what it is
load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

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

#Find the relevant info and return the top_n results
def findSimilarChunk(questionEmbedding, docEmbedding, top_n = 5):
    similarities = cosine_similarity([questionEmbedding], docEmbedding).flatten()
    topIndexes = similarities.argsort()[-top_n:][::-1]
    return topIndexes, similarities[topIndexes]


#Reading in and chunking the document here
file = open("textbook.txt", 'r', encoding='latin-1')
document = (file.read())
file.close()

chunks = splitDocument(document)
chunkEmbeddings = [createEmbedding(chunk) for chunk in chunks]

#ChatGPT Functionality starts here
question = ""
print("Type quit to exit this chatbot\n")
while question.lower() != "quit" :
    question = input("Question\n")

    if question.lower() != "quit":

        #Getting the most relevant info out of document here
        questionEmbedding = createEmbedding(question)
        top_indices, top_similarities = findSimilarChunk(questionEmbedding, chunkEmbeddings)
        text = "\n\n".join([chunks[i] for i in top_indices])

        #Generate the answer here
        response = openai.ChatCompletion.create(
                model = "gpt-3.5-turbo",
                messages = [
                    {"role" : "system", "content" : text},
                    {"role": "user", "content": question}
                ],
                max_tokens = 256
            )

        answer = response.choices[0].message['content'].strip()
        print("\nAnswer")
        print(answer + "\n")