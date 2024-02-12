from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')
chat_model = ChatOpenAI(openai_api_key=api_key)

request = """Imagine you are a guy on hinge. This is the conversation you are having with Alison. "You: How do you like living in downtown sac
Alison: I love downtown sac. There’s a lot to do and I’m always finding new things. Do you live there too or looking to move? . 
You: Just wanted to know how you like it
You: So how was growing up in chowchilla
Alison: Okay nice! . 
Alison: Chowchilla was okay. It was very very small but I enjoyed it and made really great friends. Plus I was less than a mile from all my close family . 
You: Nice! Chowchilla seems cute
You: So how do you like the food in sac compared to New York
Alison: Lol it is cute. 
Alison: Oooo good question! I miss the pizza soooo much and the bagels. I can’t find anything close to them here. But overall I like the food in Sac better. You liked this message." Give me 3 example of questions you could ask"""


result = chat_model.predict(request)
print(result)