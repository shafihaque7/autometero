// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getFirestore } from "firebase/firestore";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyC17NBzSzPZVUd8PZY0jmtWHLB5pppSyOg",
  authDomain: "hingeautomation.firebaseapp.com",
  projectId: "hingeautomation",
  storageBucket: "hingeautomation.appspot.com",
  messagingSenderId: "968993586795",
  appId: "1:968993586795:web:25aaed34307fc3cccf3b2e",
  measurementId: "G-65GDBLHRQY"
};

// Initialize Firebase



initializeApp(firebaseConfig);

const db = getFirestore()
export default db