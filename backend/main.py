import json

from bson.objectid import ObjectId
from flask import Flask, request
import pymongo
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
import time
from flask_cors import CORS
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
import re

# Flask initialization
app = Flask(__name__)

CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# Open AI initialization
load_dotenv()
# api_key = os.getenv('OPENAI_API_KEY')
api_key = "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"
chat_model = ChatOpenAI(openai_api_key=api_key)

# Database connection stuff
CONNECTION_STRING = "mongodb://hingeautomation:ti00pSXB7n8NGKPpDHPU0yjtrelS8N99zLf7pDNYtuEGC96mgkg2hgBh5hzoFVow6EBOJES1cpXZACDbatPdqg==@hingeautomation.mongo.cosmos.azure.com:10255/?ssl=true&retrywrites=false&replicaSet=globaldb&maxIdleTimeMS=120000&appName=@hingeautomation@"

DB_NAME = "hingeautomation"
COLLECTION_NAME = "users"

client = pymongo.MongoClient(CONNECTION_STRING)

# Create database if it doesn't exist
db = client[DB_NAME]
if DB_NAME not in client.list_database_names():
    # Create a database with 400 RU throughput that can be shared across
    # the DB's collections
    db.command({"customAction": "CreateDatabase", "offerThroughput": 400})
    print("Created db '{}' with shared throughput.\n".format(DB_NAME))
else:
    print("Using database: '{}'.\n".format(DB_NAME))


# Create collection if it doesn't exist
collection = db[COLLECTION_NAME]
if COLLECTION_NAME not in db.list_collection_names():
    # Creates a unsharded collection that uses the DBs shared throughput
    db.command(
        {"customAction": "CreateCollection", "collection": COLLECTION_NAME}
    )
    print("Created collection '{}'.\n".format(COLLECTION_NAME))
else:
    print("Using collection: '{}'.\n".format(COLLECTION_NAME))

COLLECTION_NAME_2 = "automatedMessages"
automatedMessagesCollection = db[COLLECTION_NAME_2]
if COLLECTION_NAME_2 not in db.list_collection_names():
    # Creates a unsharded collection that uses the DBs shared throughput
    db.command(
        {"customAction": "CreateCollection", "collection": COLLECTION_NAME_2}
    )
    print("Created collection '{}'.\n".format(COLLECTION_NAME_2))
else:
    print("Using collection: '{}'.\n".format(COLLECTION_NAME_2))

COLLECTION_NAME_3 = "utils"
utilsCollection = db[COLLECTION_NAME_3]
if COLLECTION_NAME_3 not in db.list_collection_names():
    db.command(
        {"customAction": "CreateCollection", "collection": COLLECTION_NAME_3}
    )
    print("Created collection '{}'.\n".format(COLLECTION_NAME_3))
else:
    print("Using collection: '{}'.\n".format(COLLECTION_NAME_3))


# End of database connection
# Appium integration

capabilities = dict(
    platformName='Android',
    automationName='uiautomator2',
    deviceName='Android',
    language='en',
    locale='US'
)
appium_server_url = 'http://104.42.212.81:4723'
driver = webdriver.Remote(appium_server_url, options=UiAutomator2Options().load_capabilities(capabilities))

@app.route("/")
def get_all_users():
    res = []

    for user in collection.find():
        data = {
            "id": str(user["_id"]),
            "name": user["name"],
            "lastUpdated": user["lastUpdated"],
            "lastMessage": user["lastMessageShownOnHinge"],
            "unread": user["unread"]
        }
        print(user)
        res.append(data)
    return res

@app.route("/user/<user_id>")
def get_user(user_id):
    user = collection.find_one({"_id": ObjectId(user_id)})
    data = {
        "id": str(user["_id"]),
        "name": user["name"],
        "lastUpdated": user["lastUpdated"],
        "messages": user["messages"]
    }
    return data

@app.route("/getLastUpdated")
def get_last_updated():
    docs = utilsCollection.find()
    print(docs[0])
    data = {
        "lastUpdatedTimeForScraper" : docs[0]["lastUpdatedTimeForScraper"],
        "currentlyRunning" : docs[0]["currentlyRunning"]
    }
    return data



@app.route("/ai/user/<user_id>")
def get_ai_suggested_messages(user_id):

    # user = collection.find_one({"_id": ObjectId(user_id)})
    #
    # messages = user["messages"]
    #
    # messageString = ""
    # for m in messages:
    #     messageString += m["user"] + ": " + m["message"] + "\n"
    #
    #
    # requestToFormat = """Imagine you are a guy on hinge. This is the conversation you are having with {name}. "{messageString}" Give me 3 example of questions you could ask. Return in format [ "<example 1>", "<example 2>", "<example 3>" ]"""
    # request = requestToFormat.format(name=user["name"], messageString = messageString)
    #
    #
    # result = chat_model.predict(request)
    # print("result: ", str(result))
    #
    # return json.loads(result)
    print("called ai storage retrieval")
    print(user_id)
    user = automatedMessagesCollection.find_one({"_id" : ObjectId(user_id)})
    data = {
        "_id": str(user["_id"]),
        "name" : user["name"],
        "aiMessages" : user["aiMessages"],
        "aiMessageToSend" : user["aiMessageToSend"]
    }
    return data

@app.route("/ai/notifications")
def get_ai_notifications():
    users = automatedMessagesCollection.find()
    res = []
    for user in users:
        data = {
            "_id" : str(user["_id"]),
            "name" : user["name"],
            "aiMessageToSend" : user["aiMessageToSend"]
        }
        res.append(data)
    return res

@app.route("/appium/sendtext", methods=['POST'])
def send_text():
    data = request.json
    print(data.get('userId'))
    print(data.get('messageToSend'))

    user = collection.find_one({"_id": ObjectId(data.get('userId'))})
    name = user["name"]
    lastMessageShownOnHinge = user["lastMessageShownOnHinge"]
    print(lastMessageShownOnHinge)
    select_user_based_on_name_and_last_message(name, lastMessageShownOnHinge, data.get("messageToSend"))
    el = driver.find_element(by=AppiumBy.XPATH,
                             value='//android.widget.ImageView[@content-desc="Back to Matches"]')
    el.click()

    return data

def type_text(text) -> None:

    textbox = driver.find_element(by=AppiumBy.XPATH, value='//android.widget.EditText[@resource-id="co.hinge.app:id/messageComposition"]')
    textbox.send_keys(text)
    el = driver.find_element(by=AppiumBy.ID, value='co.hinge.app:id/sendMessageButton')
    el.click()

def select_user_based_on_name_and_last_message(nameToSearch, lastMessageToSearch, messageToSend):

    while True:

        usersOnScreen = driver.find_elements(by=AppiumBy.ID, value='co.hinge.app:id/textLastMessage')
        numberOfUsersOnScreen = len(usersOnScreen)

        for xPathCounter in range(1, numberOfUsersOnScreen + 1):
            xpathString = '(//android.view.ViewGroup[@resource-id="co.hinge.app:id/viewForeground"])[{0}]'.format(
                xPathCounter)

            print("xpathString: " + str(xpathString))

            try:
                el = driver.find_element(by=AppiumBy.XPATH, value=xpathString)
                name = el.find_element(by=AppiumBy.ID, value='co.hinge.app:id/textSubjectName')
                print("name text from users screen: ", name.text)

                lastMessage = el.find_element(by=AppiumBy.ID, value='co.hinge.app:id/textLastMessage')
                print(lastMessage.text)

                if nameToSearch == name.text and lastMessageToSearch == lastMessage.text:

                    el.click()
                    print("Found and clicked")
                    time.sleep(1)
                    type_text(messageToSend)
                    return



            except:
                print("Failed on xpath: " + xpathString)
                continue
        size = driver.get_window_size()
        starty = (size['height'] * 0.80)
        endy = (size['height'] * 0.50)
        startx = size['width'] / 2
        driver.swipe(startx, starty, startx, endy)
        time.sleep(2)


@app.route("/appium")
def get_appium_users():
    totalNumberOfUsers = 5
    currentUserCount = 1
    allGirls = []

    while currentUserCount <= totalNumberOfUsers:

        # Getting all of the last text messages
        usersOnScreen = driver.find_elements(by=AppiumBy.ID, value='co.hinge.app:id/textLastMessage')
        numberOfUsersOnScreen = len(usersOnScreen)
        allTextLastMessages = []
        for user in usersOnScreen:
            allTextLastMessages.append(user.text)

        for xPathCounter in range(1, numberOfUsersOnScreen + 1):
            if currentUserCount <= totalNumberOfUsers:
                print("xpathCounter: " + str(xPathCounter))
                xpathString = '(//android.view.ViewGroup[@resource-id="co.hinge.app:id/viewForeground"])[{0}]'.format(
                    xPathCounter)

                print("xpathString: " + str(xpathString))

                try:
                    el = driver.find_element(by=AppiumBy.XPATH, value=xpathString)
                    name = el.find_element(by=AppiumBy.ID, value='co.hinge.app:id/textSubjectName')
                    print("name text from users screen: ", name.text)

                    lastMessage = el.find_element(by=AppiumBy.ID, value='co.hinge.app:id/textLastMessage')
                    print(lastMessage.text)

                    userInfo = name.text + " : " + lastMessage.text

                    if userInfo in allGirls:
                        continue
                    else:
                        allGirls.append(userInfo)
                        currentUserCount += 1

                except:
                    print("Failed on xpath: " + xpathString)
                    continue



        # Swipe down for other users
        size = driver.get_window_size()
        starty = (size['height'] * 0.80)
        endy = (size['height'] * 0.50)
        startx = size['width'] / 2
        driver.swipe(startx, starty, startx, endy)

    print(allGirls)
    print(len(allGirls))
    return allGirls


if __name__ == "__main__":
    # app.run(debug=True, port=5000)
    # app.run()
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))