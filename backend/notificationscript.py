from script import *
from datetime import timedelta

if __name__ == '__main__':
    docs = get_ai_messages_to_send(collection, automatedMessagesCollection)

    for doc in docs:
        # print(doc)

        sendTime = doc["sendTime"]

        dateTimeObject = datetime.strptime(sendTime, "%m/%d/%Y %I:%M:%S %p")

        diff = dateTimeObject - datetime.now()
        print("diff", diff)

        #Send notification 1 hour before
        if (timedelta(minutes=60) <= diff <= timedelta(minutes=61)):
            send_notification(utilsCollection, "Sending Notification to "+ doc["name"] + " in 1 hour!", doc["aiMessageToSend"])






