from openai import OpenAI
client = OpenAI()



def start_gpt():
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system",
             "content": "Imagine you are a guy on hinge, start a conversation and respond. The only thing you know about the girl is that she lives in Sacramento."},
        ]
    )
    return response.choices[0].message.content.strip()

def chat_with_gpt(prompt):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content.strip()


if __name__ == "__main__":
    print("Chatbot: ", start_gpt())
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["quit", "exit", "bye"]:
            break
        response = chat_with_gpt(user_input)
        print("Chatbot: ", response)