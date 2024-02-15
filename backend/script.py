import pymongo
from appium import webdriver
from appium.options.android import UiAutomator2Options
import time
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


def scroll_up_to_top(driver) -> None:
    while True:
        try:
            size = driver.get_window_size()
            starty = (size['height'] * 0.50)
            endy = (size['height'] * 0.80)
            startx = size['width'] / 2
            driver.swipe(startx, starty, startx, endy)
            time.sleep(1)
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

def test_select_first_10_user_and_read_message(driver) -> None:
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

                else:
                    if doc["lastMessageShownOnHinge"] == lastMessageText:
                        continue
                    else:
                        # Update the document
                        el.click()
                        time.sleep(1)
                        read_messages(driver, lastMessageText, doc)


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

if __name__ == "__main__":
    while True:
        driver = webdriver.Remote(appium_server_url, options=UiAutomator2Options().load_capabilities(capabilities))
        scroll_up_to_top(driver)
        test_select_first_10_user_and_read_message(driver)
        scroll_up_to_top(driver)
        # driver.quit()
        time.sleep(600)

    # Delete everything from database

