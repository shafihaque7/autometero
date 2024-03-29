from script import *
from datetime import timedelta
import asyncio
loop = asyncio.get_event_loop()

if __name__ == '__main__':
    docs = get_ai_messages_to_send(collection, automatedMessagesCollection)

    for doc in docs:
        print(doc)

        sendTime = doc["sendTime"]

        dateTimeObject = datetime.strptime(sendTime, "%m/%d/%Y %I:%M:%S %p")

        diff = dateTimeObject - datetime.now()
        print("diff", diff)

        #Send notification 1 hour before
        if (timedelta(minutes=5) <= diff <= timedelta(minutes=6)):
            send_notification(utilsCollection, "Sending Notification to "+ doc["name"] + " in 5 minutes!", doc["aiMessageToSend"])

        # Send Notification now
        if timedelta(minutes=0) <= diff <= timedelta(minutes=1):
            send_notification(utilsCollection, "Sending Notification to " + doc["name"] + "!",
                              doc["aiMessageToSend"])

            # Moving the notification to 3 hours after
            dt_string = (datetime.now() + timedelta(hours=3)).strftime("%m/%d/%Y %I:%M:%S %p")
            sendTime = {
                "sendTime": dt_string
            }
            automatedMessagesCollection.update_one(doc, {"$set": sendTime})

            #Commented out code for sending actual message

            # driver = webdriver.Remote(appium_server_url, options=UiAutomator2Options().load_capabilities(capabilities))
            #
            #
            # user = collection.find_one({"_id": doc["_id"]})
            # name = user["name"]
            # lastMessageShownOnHinge = user["lastMessageShownOnHinge"]
            # print(lastMessageShownOnHinge)
            # select_user_based_on_name_and_last_message(driver, name, lastMessageShownOnHinge)
            # type_text(driver, doc["aiMessageToSend"])
            #
            # scrapedUser = read_messages(driver, lastMessageShownOnHinge, user, collection)
            #
            # el = driver.find_element(by=AppiumBy.XPATH,
            #                          value='//android.widget.ImageView[@content-desc="Back to Matches"]')
            # el.click()
            # loop.run_until_complete(async_scroll_up_to_top(driver))

            #End of sending actual text message









