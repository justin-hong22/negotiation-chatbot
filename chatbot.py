import openai
import glob
openai.api_key = <CHANGE ME>

#Reading in the transcript here
file = open("transcript.txt", 'r')
text = (file.read())
file.close()

#ChatGPT Functionality starts here
question = ""
print("Type quit to exit this chatbot\n")
while question.lower() != "quit" :
    question = input("Question\n")

    if question.lower() != "quit":
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