import pymongo
from appium import webdriver
from appium.options.android import UiAutomator2Options
import time
from openaiinternal import chatgptcall
from bson.objectid import ObjectId
from datetime import datetime


from appium.webdriver.common.appiumby import AppiumBy

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


def store_timestamp():
    dt_string = datetime.now().strftime("%m/%d/%Y %I:%M:%S %p")
    utilsCollection.delete_many({})
    lastUpdatedTime = {"lastUpdatedTimeForScraper": dt_string}
    utilsCollection.insert_one(lastUpdatedTime)


def scroll_up_to_top(driver) -> None:
    # Scroll up for up to 30 seconds
    t_end = time.time() + 30
    while time.time() < t_end:
        try:
            size = driver.get_window_size()
            starty = (size['height'] * 0.50)
            endy = (size['height'] * 0.80)
            startx = size['width'] / 2
            driver.swipe(startx, starty, startx, endy)
            # time.sleep(1)
            el = driver.find_element(by=AppiumBy.ID, value='co.hinge.app:id/section_title')
            sectionTitle = el.text
            if sectionTitle[:9] == "Your turn":
                break
        except:
            continue

def read_messages(driver, lastMessageShownOnHinge, doc) -> None:

    el = driver.find_element(by=AppiumBy.XPATH,
                                  value='//android.widget.TextView[@resource-id="co.hinge.app:id/pageTitle"]')


    nameOfThePerson = el.text

    messages = []

    size = driver.get_window_size()

    while not driver.find_elements(by=AppiumBy.ID, value='co.hinge.app:id/liked_answer') and not driver.find_elements(by=AppiumBy.ID, value='co.hinge.app:id/liked_photo'):

        elements = driver.find_elements(by=AppiumBy.XPATH,
                                             value="//android.widget.TextView[@resource-id='co.hinge.app:id/chatBubble']")
        innerList = []
        for element in elements:
            # print(element.tag_name)
            innerList.append(element.tag_name)

        messages = innerList + messages
        # Scroll up all the way
        starty = (size['height'] * 0.30)
        endy = (size['height'] * 0.60)
        startx = size['width'] / 2
        driver.swipe(startx, starty, startx, endy)
        time.sleep(2)
    elements = driver.find_elements(by=AppiumBy.XPATH,
                                         value="//android.widget.TextView[@resource-id='co.hinge.app:id/chatBubble']")
    innerList = []
    for element in elements:
        # print(element.tag_name)
        innerList.append(element.tag_name)

    messages = innerList + messages
    # Scroll up all the way
    starty = (size['height'] * 0.30)
    endy = (size['height'] * 0.70)
    startx = size['width'] / 2
    driver.swipe(startx, starty, startx, endy)
    time.sleep(2)

    order = 1

    messagesSorted = []
    for m in list(dict.fromkeys(messages)):
        print(m)

        res = m.split(": ",1)
        data = {"user": res[0], "message": res[1], "timestamp": datetime.now()}
        messagesSorted.append(data)
        order+=1

    unread = 0
    if len(messagesSorted) > 0 and messagesSorted[-1]["user"] != "You":
        unread = 1

    user = {
        "name": nameOfThePerson,
        "lastMessageShownOnHinge": lastMessageShownOnHinge,
        "lastUpdated": datetime.now(),
        "unread": unread,
        "messages": messagesSorted
    }
    if doc is None:
        collection.insert_one(user)
    else:
        collection.update_one(doc, {"$set": user})

def test_select_first_10_user_and_read_message(driver) -> bool:
    shouldRunAI = False
    totalNumberOfUsers = 10
    currentUserCount = 1
    allGirls = []

    while currentUserCount <= totalNumberOfUsers:

        #Getting all of the last text messages
        usersOnScreen = driver.find_elements(by=AppiumBy.ID, value='co.hinge.app:id/textLastMessage')
        numberOfUsersOnScreen = len(usersOnScreen)
        allTextLastMessages= []
        for user in usersOnScreen:
            allTextLastMessages.append(user.text)

        for xPathCounter in range(1, numberOfUsersOnScreen + 1):
            if currentUserCount <= totalNumberOfUsers:
                print("xpathCounter: " + str(xPathCounter))
                xpathString = '(//android.view.ViewGroup[@resource-id="co.hinge.app:id/viewForeground"])[{0}]'.format(
                    xPathCounter)

                print("xpathString: " + str(xpathString))

                nameText = None
                lastMessageText = None

                try:
                    el = driver.find_element(by=AppiumBy.XPATH, value=xpathString)
                    name = el.find_element(by=AppiumBy.ID, value='co.hinge.app:id/textSubjectName')
                    print("name text from users screen: ",name.text)
                    nameText = name.text

                    lastMessage = el.find_element(by=AppiumBy.ID, value='co.hinge.app:id/textLastMessage')
                    print(lastMessage.text)
                    lastMessageText = lastMessage.text

                    userInfo = name.text + " : " + lastMessage.text

                    if userInfo in allGirls:
                        continue
                    else:
                        allGirls.append(userInfo)
                        currentUserCount += 1

                except:
                    print("Failed on xpath: " + xpathString)
                    continue


                doc = collection.find_one({"name": nameText})
                if doc is None:
                    el.click()
                    time.sleep(1)
                    read_messages(driver, lastMessageText, None)
                    shouldRunAI = True

                else:
                    if doc["lastMessageShownOnHinge"] == lastMessageText:
                        continue
                    else:
                        # Update the document
                        el.click()
                        time.sleep(1)
                        read_messages(driver, lastMessageText, doc)
                        shouldRunAI = True


                el = driver.find_element(by=AppiumBy.XPATH,
                                              value='//android.widget.ImageView[@content-desc="Back to Matches"]')
                el.click()


        # Swipe down for other users
        size = driver.get_window_size()
        starty = (size['height'] * 0.80)
        endy = (size['height'] * 0.50)
        startx = size['width'] / 2
        driver.swipe(startx, starty, startx, endy)
        time.sleep(2)
        return shouldRunAI

def store_ai_messages() -> None:
    # users = collection.find({"unread" : 1})
    users = collection.find()
    print(users)
    for user in users:
        automatedMessagesCollection.delete_many({"_id": ObjectId(user["_id"])})
        res = chatgptcall(user)
        # print(res)
        # time.sleep(1)
        print(user)

        userData = {
            "_id" : user["_id"],
            "name": user["name"],
            "aiMessages" : res,
            "aiMessageToSend" : res[0] if len(res) > 0 else None
        }

        automatedMessagesCollection.insert_one(userData)
        time.sleep(2)



if __name__ == "__main__":
    totalNumberOfTimesRam = 0
    while True:
        driver = webdriver.Remote(appium_server_url, options=UiAutomator2Options().load_capabilities(capabilities))
        scroll_up_to_top(driver)
        shouldRunAI = test_select_first_10_user_and_read_message(driver)
        scroll_up_to_top(driver)
        totalNumberOfTimesRam +=1
        print("Total number of times the autoscraper ran: ",totalNumberOfTimesRam)
        driver.quit()
        if shouldRunAI:
            try:
                store_ai_messages()
            except:
                print("AI failed")

        store_timestamp()
        time.sleep(600)

    # Delete everything from database

