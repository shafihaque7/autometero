import os
import re

#
# someList = ['Laura : There used to be a place called…', 'LaShia : Start the chat with LaShia', 'Alanis : I started choir in middle school…', 'Ena : So did you grow up around sac…', 'melissa : Who do you think is the best…', 'Cam : How do you like living in…', 'Amanda : Nice! What was growing up in…', 'Akshita : What do you hate about Davis…', 'Lauren : I am guessing you hate…', 'Kate : How do you like living in…', 'Arabella : Nice! So is there a lot of great…', 'Kam : Nice! So approximately how many…', 'Nikole : How do you like having a twin…', 'Haley : 559-691-9929 :)', 'Camilla : I like the extreme ones like at…', "Sonia : I'm a transfer student from the…", 'Amy : So how do you like living in…', 'Danielle : So out of Davis and Roseville,…', 'Adrianne : I wanna know more about your…', 'Alison : I could go on and on. Text me…', 'sophie : I am guessing you sneak thing…', 'Mikayla : What are you looking for on…', 'Maddie : Guessing you hate it then?', 'Madison : My guess would be Zach Bryan ', 'Manpreet : How was your experience in csu…', 'Araceli : What about if you had all the…', 'Addy : So what’s your favorite type of…', 'Claire : You get a lot of takeouts?', 'Nicole : (530)\xa0341-2327', 'Morgan : Wbu? You know how to surf?', 'Maria : Can I also ask how your name is…', 'Peyton : How do you like living in…', 'Emma : Start the chat with Emma', 'thida <3 : So is there a lot of abandoned…', 'Jasmine : Which one of the three is your…', 'Emily : I love visiting my best friend…', 'Jenna : My guess is you absolutely…', 'jean : My guess would be tequila', 'Valeria : Hey shafi sorry for the late…', 'Gabby : How do you like living in Davis…', 'Amelia : hmm idk theres pros and cons to…', 'Adie : Is corn your favorite…', 'Haimanot : I am big into food! There is a…', 'Sri : How do you like living in…', 'Claire : So how good are you at…', 'Annabelle : What’s your favorite activity…', 'Mak : How do you like living in Cirby…', 'Faith : Have you ever made fries…', 'Vicky : How do you like living in sac', 'Isabelle : Do you thing Santana row mall…', 'Catherine : Monaco, bad bunny. Hbu?', 'Monica : What’s your favorite Nathan…', 'Iryna : Start the chat with Iryna']
#
# print(len(someList))
# #
# # for s in someList:
# #     res = s.split(": ",1)
# #     print(res[0])
#
#
#
# print("The code works pretty instantly ")
#
#
# CONNECTION_STRING = os.environ.get("COSMOS_CONNECTION_STRING")
# print(CONNECTION_STRING)


s = """ 1. "What are some of your favorite food spots in Sacramento that you've discovered so far?"
2. "Have you found any hidden gem restaurants or cafes in downtown Sac that you would recommend?"
3. "Since you mentioned missing the pizza and bagels from New York, have you found any decent substitutes here in Sacramento or do you have any tips for finding good pizza and bagels in the area?" """


quoted = re.compile('"(.*?)"')
for value in quoted.findall(s):
    print (value)


# messages = [
#     {
#         "user": "You",
#         "message": "How do you like living in downtown",
#         "timestamp": {
#             "$date": 1706625537609
#         }
#     },
#     {
#         "user": "Alanis",
#         "message": "Good, I love it :). ",
#         "timestamp": {
#             "$date": 1706625537609
#         }
#     },
#     {
#         "user": "You",
#         "message": "So how long have you been singing? Is it all your life",
#         "timestamp": {
#             "$date": 1706625537609
#         }
#     },
#     {
#         "user": "Alanis",
#         "message": "Since forever . ",
#         "timestamp": {
#             "$date": 1706625537609
#         }
#     },
#     {
#         "user": "Alanis",
#         "message": "I started choir in middle school but I’ve been singing ever since I can remember . ",
#         "timestamp": {
#             "$date": 1706625537609
#         }
#     }
# ]
#
# res = ""
#
# for m in messages:
#     res += m["user"] + ": " + m["message"] +"\n"
#
# print(res)
