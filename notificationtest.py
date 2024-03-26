import firebase_admin
from firebase_admin import credentials, messaging

cred = credentials.Certificate("firebase-admin-credential.json")
firebase_admin.initialize_app(cred)

tokens = [
    "e-QLDVlPkFHQX65h4eoBWG:APA91bFvoDzURmc6QenaVcfjU5693eqk5XcJ1BqRTYEiePn6nfjevnvoxvRlWpmviWgNlkljix7pKun2bDFwvSf7n708jKT42_LjSlYz8KP01aKnrT936mTYWhVmjAMJ-ysg5jSGIUca"]

message = messaging.MulticastMessage(
    notification=messaging.Notification(
        title="Place where ffffnotification is coming",
        body="Some bodyfffffff"
    ),
    tokens=tokens
)
messaging.send_multicast(message)
