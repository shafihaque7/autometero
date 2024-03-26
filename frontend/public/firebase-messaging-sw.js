// Give the service worker access to Firebase Messaging.
// Note that you can only use Firebase Messaging here. Other Firebase libraries
// are not available in the service worker.
importScripts('https://www.gstatic.com/firebasejs/8.10.1/firebase-app.js');
importScripts('https://www.gstatic.com/firebasejs/8.10.1/firebase-messaging.js');

// Initialize the Firebase app in the service worker by passing in
// your app's Firebase config object.
// https://firebase.google.com/docs/web/setup#config-object
firebase.initializeApp({
  apiKey: "AIzaSyC17NBzSzPZVUd8PZY0jmtWHLB5pppSyOg",
  authDomain: "hingeautomation.firebaseapp.com",
  projectId: "hingeautomation",
  storageBucket: "hingeautomation.appspot.com",
  messagingSenderId: "968993586795",
  appId: "1:968993586795:web:25aaed34307fc3cccf3b2e",
  measurementId: "G-65GDBLHRQY"
});

// Retrieve an instance of Firebase Messaging so that it can handle background
// messages.
const messaging = firebase.messaging();

// messaging.onBackgroundMessage((payload) => {
//   console.log(
//     '[firebase-messaging-sw.js] Received background message ',
//     payload
//   );
//   // Customize notification here
//   const notificationTitle = payload.notification.title;
//   const notificationOptions = {
//     body: payload.notification.body,
//     icon: '/icon.png'
//   };
//
//   self.registration.showNotification(notificationTitle, notificationOptions);
// });
