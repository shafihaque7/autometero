import pymongo
from appium import webdriver
from appium.options.android import UiAutomator2Options
import time
import openaiinternal
from bson.objectid import ObjectId
from datetime import datetime

from appium.webdriver.common.appiumby import AppiumBy
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

async def async_scroll_up_to_top(driver) -> None:
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



def store_timestamp(utilsCollection):
    dt_string = datetime.now().strftime("%m/%d/%Y %I:%M:%S %p")
    doc = utilsCollection.find()[0]
    lastUpdatedTime = {
        "lastUpdatedTimeForScraper": dt_string,
        "currentlyRunning": False
    }
    utilsCollection.update_one(doc, {"$set": lastUpdatedTime})

def read_messages(driver, lastMessageShownOnHinge, doc, collection) -> None:

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

    return user

def type_text(driver, text) -> None:

    textbox = driver.find_element(by=AppiumBy.XPATH, value='//android.widget.EditText[@resource-id="co.hinge.app:id/messageComposition"]')
    textbox.send_keys(text)
    el = driver.find_element(by=AppiumBy.ID, value='co.hinge.app:id/sendMessageButton')
    el.click()

def select_user_based_on_name(driver, nameToSearch):
    select_user_based_on_name_and_last_message(driver, nameToSearch)
def select_user_based_on_name_and_last_message(driver, nameToSearch, lastMessageToSearch=None):

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

                if lastMessageToSearch == None and nameToSearch == name.text:
                    el.click()
                    print("Found and clicked")
                    time.sleep(1)
                    return

                elif lastMessageToSearch != None and nameToSearch == name.text and lastMessageToSearch == lastMessage.text:

                    el.click()
                    print("Found and clicked")
                    time.sleep(1)
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

def test_select_first_10_user_and_read_message(driver, collection) -> bool:
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
                    read_messages(driver, lastMessageText, None, collection)
                    shouldRunAI = True

                else:
                    if doc["lastMessageShownOnHinge"] == lastMessageText:
                        continue
                    else:
                        # Update the document
                        el.click()
                        time.sleep(1)
                        read_messages(driver, lastMessageText, doc, collection)
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

def store_ai_messages(collection, automatedMessagesCollection, utilsCollection) -> None:
    # users = collection.find({"unread" : 1})
    users = collection.find()
    print(users)
    for user in users:
        automatedMessagesCollection.delete_many({"_id": ObjectId(user["_id"])})
        res = openaiinternal.chatgptcall(user, 3, utilsCollection)
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

def enable_currently_running_status(utilsCollection):
    doc = utilsCollection.find()[0]
    utilsCollection.update_one(doc, {"$set": {"currentlyRunning": True}})

