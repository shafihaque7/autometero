from openai import OpenAI
client = OpenAI()



def start_gpt():
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system",
             "content": "You are a guy on hinge, start the conversation and the only thing you know is that the girl's name is Alanis and she is from sacramento. Have a conversation then eventually ask out for drinks after 5 to 10 messages. "},
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