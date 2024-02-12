import unittest
import time
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from datetime import datetime

capabilities = dict(
    platformName='Android',
    automationName='uiautomator2',
    deviceName='Android',
    language='en',
    locale='US'
)

# appium_server_url = 'http://localhost:4723'
appium_server_url = 'http://104.42.212.81:4723'
from random import randint

import pymongo

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






class TestAppium(unittest.TestCase):
    def setUp(self) -> None:
        self.driver = webdriver.Remote(appium_server_url, options=UiAutomator2Options().load_capabilities(capabilities))

    def tearDown(self) -> None:
        if self.driver:
            self.driver.quit()


    def test_get_all_elements(self) -> None:
        size = self.driver.get_window_size()
        starty = (size['height'] * 0.80)
        endy = (size['height'] * 0.50)
        startx = size['width'] / 2
        self.driver.swipe(startx, starty, startx, endy)



    def test_type_text(self) -> None:

        textbox = self.driver.find_element(by=AppiumBy.XPATH, value='//android.widget.EditText[@resource-id="co.hinge.app:id/messageComposition"]')
        textbox.send_keys("That's a handsome dude")

    def test_select_user_based_on_name_and_last_message(self) -> None:
        nameToSearch = "Alanis"
        lastMessageToSearch = "I started choir in middle school…"

        while True:

            usersOnScreen = self.driver.find_elements(by=AppiumBy.ID, value='co.hinge.app:id/textLastMessage')
            numberOfUsersOnScreen = len(usersOnScreen)

            for xPathCounter in range(1, numberOfUsersOnScreen + 1):
                xpathString = '(//android.view.ViewGroup[@resource-id="co.hinge.app:id/viewForeground"])[{0}]'.format(
                    xPathCounter)

                print("xpathString: " + str(xpathString))

                try:
                    el = self.driver.find_element(by=AppiumBy.XPATH, value=xpathString)
                    name = el.find_element(by=AppiumBy.ID, value='co.hinge.app:id/textSubjectName')
                    print("name text from users screen: ", name.text)

                    lastMessage = el.find_element(by=AppiumBy.ID, value='co.hinge.app:id/textLastMessage')
                    print(lastMessage.text)

                    if nameToSearch == name.text and lastMessageToSearch == lastMessage.text:

                        el.click()
                        print("Found and clicked")
                        return



                except:
                    print("Failed on xpath: " + xpathString)
                    continue
            size = self.driver.get_window_size()
            starty = (size['height'] * 0.80)
            endy = (size['height'] * 0.50)
            startx = size['width'] / 2
            self.driver.swipe(startx, starty, startx, endy)
            time.sleep(2)

    def test_select_first_50_user_and_read_message(self) -> None:
        totalNumberOfUsers = 50
        currentUserCount = 1
        allGirls = []

        while currentUserCount <= totalNumberOfUsers:

            #Getting all of the last text messages
            usersOnScreen = self.driver.find_elements(by=AppiumBy.ID, value='co.hinge.app:id/textLastMessage')
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

                    lastMessageText = None

                    try:
                        el = self.driver.find_element(by=AppiumBy.XPATH, value=xpathString)
                        name = el.find_element(by=AppiumBy.ID, value='co.hinge.app:id/textSubjectName')
                        print("name text from users screen: ",name.text)

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

                    el.click()
                    time.sleep(1)

                    self.test_read_messages(lastMessageText)


                    el = self.driver.find_element(by=AppiumBy.XPATH,
                                                  value='//android.widget.ImageView[@content-desc="Back to Matches"]')
                    el.click()


            # Swipe down for other users
            size = self.driver.get_window_size()
            starty = (size['height'] * 0.80)
            endy = (size['height'] * 0.50)
            startx = size['width'] / 2
            self.driver.swipe(startx, starty, startx, endy)
            time.sleep(2)
        print(allGirls)
        print(len(allGirls))









    def test_read_messages(self, lastMessageShownOnHinge) -> None:

        el = self.driver.find_element(by=AppiumBy.XPATH,
                                      value='//android.widget.TextView[@resource-id="co.hinge.app:id/pageTitle"]')


        nameOfThePerson = el.text

        messages = []

        size = self.driver.get_window_size()

        while not self.driver.find_elements(by=AppiumBy.ID, value='co.hinge.app:id/liked_answer') and not self.driver.find_elements(by=AppiumBy.ID, value='co.hinge.app:id/liked_photo'):

            elements = self.driver.find_elements(by=AppiumBy.XPATH,
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
            self.driver.swipe(startx, starty, startx, endy)
            time.sleep(2)
        elements = self.driver.find_elements(by=AppiumBy.XPATH,
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
        self.driver.swipe(startx, starty, startx, endy)
        time.sleep(2)

        order = 1

        messagesSorted = []
        for m in list(dict.fromkeys(messages)):
            print(m)

            res = m.split(": ",1)
            data = {"user": res[0], "message": res[1], "timestamp": datetime.now()}
            messagesSorted.append(data)
            order+=1

        user = {
            "name": nameOfThePerson,
            "lastMessageShownOnHinge": lastMessageShownOnHinge,
            "lastUpdated": datetime.now(),
            "messages": messagesSorted
        }
        collection.insert_one(user)








if __name__ == '__main__':
    unittest.main()