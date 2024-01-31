from random import randint
import time
from datetime import datetime

import pymongo

CONNECTION_STRING = "mongodb://hingeautomation:ti00pSXB7n8NGKPpDHPU0yjtrelS8N99zLf7pDNYtuEGC96mgkg2hgBh5hzoFVow6EBOJES1cpXZACDbatPdqg==@hingeautomation.mongo.cosmos.azure.com:10255/?ssl=true&retrywrites=false&replicaSet=globaldb&maxIdleTimeMS=120000&appName=@hingeautomation@"


DB_NAME = "adventureworks"
COLLECTION_NAME = "products"

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



"""Create new document and upsert (create or replace) to collection"""
product = {
    "category": "gear-surf-surfboards",
    "name": "Yamba Surfboard-{}".format(randint(50, 5000)),
    "quantity": 1,
    "sale": False,
    "lastUpdated": datetime.now(),
    "messages": [{"user":"You", "msg": "hello how are you"}, {"user":"Haley", "msg": "Very goodjjjjj"}]
}
# result = collection.update_one(
#     {"name": product["name"]}, {"$set": product}, upsert=True
# )

collection.insert_one(product)
# print("Upserted document with _id {}\n".format(result.upserted_id))


for x in collection.find():
    print(x)