from bson import ObjectId
from flask import Flask
app = Flask(__name__)
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

@app.route("/")
def get_all_users():
    res = []

    for user in collection.find():
        data = {
            "id": str(user["_id"]),
            "name": user["name"],
            "lastUpdated": user["lastUpdated"],
            "messages": user["messages"]
        }
        print(user)
        res.append(data)
    return res

@app.route("/user/<user_id>")
def get_user(user_id):
    user = collection.find_one({"_id": ObjectId(user_id)})
    data = {
        "id": str(user["_id"]),
        "name": user["name"],
        "lastUpdated": user["lastUpdated"],
        "messages": user["messages"]
    }
    return data
