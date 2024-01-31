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

appium_server_url = 'http://localhost:4723'



import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Use a service account.
cred = credentials.Certificate('firebase-admin-credential.json')

app = firebase_admin.initialize_app(cred)

db = firestore.client()

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



    def test_select_user(self) -> None:

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

                    try:
                        el = self.driver.find_element(by=AppiumBy.XPATH, value=xpathString)
                        name = el.find_element(by=AppiumBy.ID, value='co.hinge.app:id/textSubjectName')
                        print("name text from users screen: ",name.text)

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

                    el.click()
                    time.sleep(1)

                    self.test_read_messages()


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









    def test_read_messages(self) -> None:

        el = self.driver.find_element(by=AppiumBy.XPATH,
                                      value='//android.widget.TextView[@resource-id="co.hinge.app:id/pageTitle"]')
        doc_ref = db.collection("users").document()
        doc_ref.set({"name": el.text, "lastUpdated": datetime.now()})

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
        for m in list(dict.fromkeys(messages)):
            print(m)

            res = m.split(": ",1)
            data = {"user": res[0], "message": res[1], "timestamp": datetime.now(), "order": order}
            doc_ref.collection("messages").document().set(data)
            order+=1




if __name__ == '__main__':
    unittest.main()