import unittest
import time
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy

capabilities = dict(
    platformName='Android',
    automationName='uiautomator2',
    deviceName='Android',
    language='en',
    locale='US'
)

appium_server_url = 'http://localhost:4723'

class TestAppium(unittest.TestCase):
    def setUp(self) -> None:
        self.driver = webdriver.Remote(appium_server_url, options=UiAutomator2Options().load_capabilities(capabilities))

    def tearDown(self) -> None:
        if self.driver:
            self.driver.quit()

    def test_find_battery(self) -> None:

        messages = []

        size = self.driver.get_window_size()

        while not self.driver.find_elements(by=AppiumBy.XPATH, value='//android.widget.TextView[@resource-id="co.hinge.app:id/blurb"]'):
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


        for m in list(dict.fromkeys(messages)):
            print(m)


        # Scroll down
        # starty = (size['height'] * 0.80)
        # endy = (size['height'] * 0.40)
        # startx = size['width'] / 2
        # self.driver.swipe(startx, starty, startx, endy)

        # self.driver.swipe(0, 1000, 0, 500)
        # el = self.driver.find_element(by=AppiumBy.XPATH, value='//android.widget.TextView[@content-desc="Hinge"]')
        # el.click()
        # time.sleep(5)
        # el = self.driver.find_element(by=AppiumBy.XPATH, value='(//android.view.ViewGroup[@resource-id="co.hinge.app:id/viewForeground"])[1]')
        # el.click()
        #
        # time.sleep(5)
        #
        #
        # elements = self.driver.find_elements(by=AppiumBy.XPATH, value="//android.widget.TextView[@resource-id='co.hinge.app:id/chatBubble']")
        # for element in elements:
        #     print(element.tag_name)

if __name__ == '__main__':
    unittest.main()