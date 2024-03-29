from script import *
from datetime import timedelta
import asyncio
loop = asyncio.get_event_loop()

if __name__ == '__main__':

    numberOfTimesRanNotificationScript = 0

    while True:
        run_notification_script(collection, automatedMessagesCollection, utilsCollection)
        numberOfTimesRanNotificationScript +=1
        print("Number of times notification script ran, ", numberOfTimesRanNotificationScript)
        time.sleep(60)









