import pymongo
from appium import webdriver
from appium.options.android import UiAutomator2Options
import time
import openaiinternal
from bson.objectid import ObjectId
from datetime import datetime

from appium.webdriver.common.appiumby import AppiumBy
from appiumscripts import *

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



if __name__ == "__main__":

    totalNumberOfTimesRam = 0
    while True:
        enable_currently_running_status(utilsCollection)
        driver = webdriver.Remote(appium_server_url, options=UiAutomator2Options().load_capabilities(capabilities))
        scroll_up_to_top(driver)
        shouldRunAI = test_select_first_10_user_and_read_message(driver, collection)
        scroll_up_to_top(driver)
        totalNumberOfTimesRam +=1
        print("Total number of times the autoscraper ran: ",totalNumberOfTimesRam)
        driver.quit()
        if shouldRunAI:
            try:
                store_ai_messages(collection, automatedMessagesCollection, utilsCollection)
            except:
                print("AI failed")

        store_timestamp(utilsCollection)
        time.sleep(600)


