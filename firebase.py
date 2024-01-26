from datetime import datetime

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Use a service account.
cred = credentials.Certificate('firebase-admin-credential.json')

app = firebase_admin.initialize_app(cred)

db = firestore.client()

# doc_ref = db.collection("users").document("alovelace")
# doc_ref.set({"first": "Ada", "last": "Lovelace", "born": 1815})

# doc_ref = db.collection("users").document("aturing")
# doc_ref.set({"first": "Alan", "middle": "Mathison", "last": "Turing", "born": 1912})



users_ref = db.collection("users")
docs = users_ref.stream()

for doc in docs:
    print(f"{doc.id} => {doc.to_dict()}")
    for docinner in db.collection("users").document(doc.id).collection("messages").order_by("order").stream():
        print(f"{docinner.to_dict()}")


# data = {"user": "Me", "message": "Hello", "timestamp": datetime.now()}
#
# docs2 = db.collection("users").document("alovelace").collection("messages").document().set(data)
