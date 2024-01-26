from flask import Flask
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
app = Flask(__name__)

# Use a service account.
cred = credentials.Certificate('firebase-admin-credential.json')

appfirebase = firebase_admin.initialize_app(cred)

db = firestore.client()





@app.route("/")
def hello_world():

    users_ref = db.collection("users")
    docs = users_ref.stream()
    users = []
    for doc in docs:
        print(f"{doc.id} => {doc.to_dict()}")
        users.append(doc.id)
    return users