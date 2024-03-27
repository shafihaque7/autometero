import firebase_admin
from firebase_admin import credentials, messaging

cred = credentials.Certificate("firebase-admin-credential.json")
firebase_admin.initialize_app(cred)

tokens = [
    "eqhgvVpD8EMRvOoSkw-xZ4:APA91bEhIzWIFqGdk2-xCwyV64XWACitqRba0QWQt5Whip6qzCRdSOZRD_RgDJxjz9xdxEgK6RTsrDSnJStt2Sz_gBJ6CB65_pI6JN3PAIkY6btliPI8_jkqJJbJXgO4WpU7S-NnsmMB"]

message = messaging.MulticastMessage(
    notification=messaging.Notification(
        title="Place where ffffnotification is coming",
        body="Some bodyfffffff"
    ),
    tokens=tokens
)
messaging.send_multicast(message)
