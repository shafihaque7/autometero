import json
from langchain_openai import ChatOpenAI

api_key = "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"
chat_model = ChatOpenAI(openai_api_key=api_key)
def chatgptcall(user, number, utilsCollection):
    messages = user["messages"]
    messageString = ""
    for m in messages:
        messageString += m["user"] + ": " + m["message"] + "\n"

    # requestToFormat = """Imagine you are a guy on hinge. This is the conversation you are having with {name}. "{messageString}" Give me {number} example of questions you could ask. Return in format [ "<example 1>", "<example 2>", "<example 3>" ]"""
    requestToFormat = get_chatgpt_prompt(utilsCollection)
    request = requestToFormat.format(name=user["name"], messageString=messageString, number=str(number))
    print(request)

    result = chat_model.predict(request)
    return json.loads(result)

def get_chatgpt_prompt(utilsCollection):
    doc = utilsCollection.find()[0]
    return doc["chatgptPrompt"]