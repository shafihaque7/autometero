import { doc, getDoc, getDocs, collection, query, addDoc, orderBy } from "firebase/firestore"
// the firestore instance
import db from '../firebaseInit'
import axios from "axios"
import { IConversation } from "@src/types";

export const defaultSettings = [
  {
    lastSeen: false,
    readReceipt: false,
    joiningGroups: false,
    privateMessages: false,
    darkMode: false,
    borderedTheme: false,
    allowNotifications: false,
    keepNotifications: false,
  },
];

export const user = {
  id: 1,
  firstName: "Dawn",
  lastSeen: new Date(),
  lastName: "Sabrina",
  email: "sabrina@gmail.com",
  avatar:
    "https://images.unsplash.com/photo-1494790108377-be9c29b29330?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=387&q=80",
  token: "fakeToken",
  contacts: [
    {
      id: 2,
      email: "user@gmail.com",
      firstName: "Ahmed",
      lastName: "Ali",
      lastSeen: new Date(),
      avatar:
        "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=387&q=80",
    },
    {
      id: 3,
      email: "user@gmail.com",
      firstName: "Allen",
      lastName: "Carr",
      lastSeen: new Date(),
      avatar:
        "https://images.unsplash.com/photo-1463453091185-61582044d556?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=870&q=80",
    },
    {
      id: 4,
      email: "user@gmail.com",
      firstName: "Dawn",
      lastName: "Sabrina",
      lastSeen: new Date(),
      avatar:
        "https://images.unsplash.com/photo-1657214059233-5626b35eb349?ixlib=rb-1.2.1&ixid=MnwxMjA3fDF8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=436&q=80",
    },
    {
      id: 5,
      email: "user@gmail.com",
      firstName: "Dylan",
      lastName: "Billy",
      lastSeen: new Date(),
      avatar:
        "https://images.unsplash.com/photo-1522556189639-b150ed9c4330?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=387&q=80",
    },
    {
      id: 6,
      email: "user@gmail.com",
      firstName: "Elijah",
      lastName: "Sabrina",
      lastSeen: new Date(),
      avatar:
        "https://images.unsplash.com/photo-1539571696357-5a69c17a67c6?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=387&q=80",
    },
    {
      id: 7,
      email: "user@gmail.com",
      firstName: "Emma",
      lastName: "Layla",
      lastSeen: new Date(),
      avatar:
        "https://images.unsplash.com/photo-1517841905240-472988babdf9?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=387&q=80",
    },
    {
      id: 8,
      email: "user@gmail.com",
      firstName: "Evelyn",
      lastName: "Billy",
      lastSeen: new Date(),
      avatar:
        "https://images.unsplash.com/photo-1539571696357-5a69c17a67c6?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxzZWFyY2h8Nnx8cGVvcGxlfGVufDB8fDB8fA%3D%3D&auto=format&fit=crop&w=500&q=60",
    },
    {
      id: 9,
      email: "user@gmail.com",
      firstName: "Feng",
      lastName: "Zhuo",
      lastSeen: new Date(),
      avatar:
        "https://images.unsplash.com/photo-1519085360753-af0119f7cbe7?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=387&q=80",
    },
    {
      id: 10,
      email: "user@gmail.com",
      firstName: "Fung",
      lastName: "Sheng",
      lastSeen: new Date(),
      avatar:
        "https://images.pexels.com/photos/1851164/pexels-photo-1851164.jpeg?cs=srgb&dl=pexels-charles-1851164.jpg&fm=jpg",
    },
  ],
};

export const conversations : IConversation[]= [];




export const archive = [];

export const notifications = [
  {
    flag: "security",
    title: "Recent Login",
    message: "there was a recent login to you account from this device",
  },
  {
    flag: "added-to-group",
    title: "New Group",
    message: "Your friend added you to a new group",
  },
  {
    flag: "account-update",
    title: "Password Reset",
    message: "Your password has been restored successfully",
  },
  {
    flag: "security",
    title: "Recent Login",
    message: "there was a recent login to you account from this device",
  },
  {
    flag: "added-to-group",
    title: "New Group",
    message: "Your friend added you to a new group",
  },
];

export const calls = [
  {
    id: 1,
    type: "voice",
    status: "missed",
    direction: "incoming",
    date: "Dec 12, 2020",
    length: "01:12",
    members: [
      {
        id: 1,
        firstName: "Dawn",
        lastName: "Sabrina",
        lastSeen: new Date(),
        email: "sabrina@gmail.com",
        avatar:
          "https://images.unsplash.com/photo-1494790108377-be9c29b29330?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=387&q=80",
      },
      {
        id: 2,
        email: "user@gmail.com",
        firstName: "Ahmed",
        lastName: "Ali",
        lastSeen: new Date(),
        avatar:
          "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=387&q=80",
      },
    ],
    adminIds: [1],
  },

  {
    id: 2,
    type: "voice",
    status: "received",
    direction: "incoming",
    date: "Dec 12, 2020",
    length: "01:12",
    members: [
      {
        id: 1,
        firstName: "Dawn",
        lastName: "Sabrina",
        lastSeen: new Date(),
        email: "sabrina@gmail.com",
        avatar:
          "https://images.unsplash.com/photo-1494790108377-be9c29b29330?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=387&q=80",
      },
      {
        id: 2,
        email: "user@gmail.com",
        firstName: "Ahmed",
        lastName: "Ali",
        lastSeen: new Date(),
        avatar:
          "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=387&q=80",
      },
      {
        id: 3,
        email: "user@gmail.com",
        firstName: "Allen",
        lastName: "Carr",
        lastSeen: new Date(),
        avatar:
          "https://images.unsplash.com/photo-1463453091185-61582044d556?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=870&q=80",
      },
      {
        id: 9,
        email: "user@gmail.com",
        firstName: "Feng",
        lastName: "Zhuo",
        lastSeen: new Date(),
        avatar:
          "https://images.unsplash.com/photo-1519085360753-af0119f7cbe7?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=387&q=80",
      },
    ],
    adminIds: [2],
  },

  {
    id: 3,
    type: "voice",
    status: "sent",
    direction: "outgoing",
    date: "Dec 12, 2020",
    length: "01:12",
    members: [
      {
        id: 1,
        firstName: "Dawn",
        lastName: "Sabrina",
        lastSeen: new Date(),
        email: "sabrina@gmail.com",
        avatar:
          "https://images.unsplash.com/photo-1494790108377-be9c29b29330?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=387&q=80",
      },
      {
        id: 5,
        email: "user@gmail.com",
        firstName: "Dylan",
        lastName: "Billy",
        lastSeen: new Date(),
        avatar:
          "https://images.unsplash.com/photo-1522556189639-b150ed9c4330?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=387&q=80",
      },
    ],
    adminIds: [1],
  },

  {
    id: 4,
    type: "voice",
    status: "missed",
    direction: "incoming",
    date: "Dec 12, 2020",
    length: "01:12",
    members: [
      {
        id: 1,
        firstName: "Dawn",
        lastName: "Sabrina",
        lastSeen: new Date(),
        email: "sabrina@gmail.com",
        avatar:
          "https://images.unsplash.com/photo-1494790108377-be9c29b29330?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=387&q=80",
      },
      {
        id: 3,
        email: "user@gmail.com",
        firstName: "Allen",
        lastName: "Carr",
        lastSeen: new Date(),
        avatar:
          "https://images.unsplash.com/photo-1463453091185-61582044d556?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=870&q=80",
      },
    ],
    adminIds: [1],
  },

  {
    id: 5,
    type: "voice",
    status: "sent",
    direction: "outgoing",
    date: "Dec 12, 2020",
    length: "01:12",
    members: [
      {
        id: 1,
        firstName: "Dawn",
        lastName: "Sabrina",
        lastSeen: new Date(),
        email: "sabrina@gmail.com",
        avatar:
          "https://images.unsplash.com/photo-1494790108377-be9c29b29330?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=387&q=80",
      },
      {
        id: 8,
        email: "user@gmail.com",
        firstName: "Evelyn",
        lastName: "Billy",
        lastSeen: new Date(),
        avatar:
          "https://images.unsplash.com/photo-1539571696357-5a69c17a67c6?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxzZWFyY2h8Nnx8cGVvcGxlfGVufDB8fDB8fA%3D%3D&auto=format&fit=crop&w=500&q=60",
      },
      {
        id: 10,
        email: "user@gmail.com",
        firstName: "Fung",
        lastName: "Sheng",
        lastSeen: new Date(),
        avatar:
          "https://images.pexels.com/photos/1851164/pexels-photo-1851164.jpeg?cs=srgb&dl=pexels-charles-1851164.jpg&fm=jpg",
      },
    ],
    adminIds: [1],
  },
];

export const activeCall = {
  id: 6,
  type: "voice",
  status: "dialing",
  direction: "outgoing",
  date: "Dec 12, 2020",
  length: "01:12",
  members: [
    {
      id: 1,
      firstName: "Dawn",
      lastName: "Sabrina",
      lastSeen: new Date(),
      email: "sabrina@gmail.com",
      avatar:
        "https://images.unsplash.com/photo-1494790108377-be9c29b29330?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=387&q=80",
    },
    {
      id: 8,
      email: "user@gmail.com",
      firstName: "Evelyn",
      lastName: "Billy",
      lastSeen: new Date(),
      avatar:
        "https://images.unsplash.com/photo-1539571696357-5a69c17a67c6?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxzZWFyY2h8Nnx8cGVvcGxlfGVufDB8fDB8fA%3D%3D&auto=format&fit=crop&w=500&q=60",
    },
  ],
  adminIds: [1],
};

const delay = (ms: number) => new Promise((resolve) => setTimeout(resolve, ms));

export const fetchData = async () => {
  // await delay(2000);

  return await {
    data: {
      user: user,
      conversations: conversations,
      notifications: notifications,
      archivedConversations: archive,
    },
  };
};

export const updateAccount = async () => {
  // await delay(4000);

  return await {
    data: {
      detail: "Your account has been updated successfully",
    },
  };
};

export const attachments = [
  {
    id: 6,
    type: "image",
    name: "forest.jpg",
    size: "21 MB",
    url: "https://images.unsplash.com/photo-1664021975758-78d83898225d?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxlZGl0b3JpYWwtZmVlZHwxOXx8fGVufDB8fHx8&auto=format&fit=crop&w=500&q=60",
  },
  {
    id: 7,
    type: "image",
    name: "pumkins.jpg",
    size: "22 MB",
    url: "https://images.unsplash.com/photo-1664031315855-955dbca83172?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=870&q=80",
  },
  {
    id: 8,
    type: "image",
    name: "mountain.jpg",
    size: "23 MB",
    url: "https://images.unsplash.com/photo-1664091729644-07a158d7c4ca?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxlZGl0b3JpYWwtZmVlZHwyNHx8fGVufDB8fHx8&auto=format&fit=crop&w=500&q=60",
  },
  {
    id: 9,
    type: "file",
    name: "lecture-10.pdf",
    size: "52.4 MB",
    url: "https://images.unsplash.com/photo-1664091729644-07a158d7c4ca?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxlZGl0b3JpYWwtZmVlZHwyNHx8fGVufDB8fHx8&auto=format&fit=crop&w=500&q=60",
  },
  {
    id: 10,
    type: "video",
    name: "fun-video.mp4",
    size: "11.4 MB",
    url: "https://images.unsplash.com/photo-1559705421-4ae9bf6fabb5?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=870&q=80",
  },
];

const allUsersResponse = await axios.get("http://104.42.212.81:8080")
const allUsers = allUsersResponse.data
let idNumber = 1
let contactsNumber :number = 11
allUsers.forEach(function(user: any){
  const userData: IConversation = {
    id: idNumber +=1,
    objectId: user["id"],
    type: "couple",
    draftMessage: "",
    contacts: [
    {
      id: contactsNumber,
      email: "user@gmail.com",
      firstName: user["name"],
      lastName: "",
      lastSeen: new Date(),
      avatar:
        "https://images.unsplash.com/photo-1522556189639-b150ed9c4330?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=387&q=80",
    },
    {
      id: 1,
      firstName: "Dawn",
      lastName: "Sabrina",
      lastSeen: new Date(),
      email: "sabrina@gmail.com",
      avatar:
        "https://images.unsplash.com/photo-1494790108377-be9c29b29330?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=387&q=80",
    },
  ],
    messages: [
    {
      id: 1,
      content: user["lastMessage"],
      date: "1:00 pm",
      state: "read",
      sender: {
        id: contactsNumber+=1,
        email: "user@gmail.com",
        firstName: user["firstName"],
        lastName: "",
        lastSeen: new Date(),
        avatar:
          "https://images.unsplash.com/photo-1522556189639-b150ed9c4330?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=387&q=80",
      },
    },
  ]
  }
  conversations.push(userData)



})





// const axiosData = await axios.get("http://127.0.0.1:5000/user/65b97b812d5ee8a9173907ec")
// const serverMessages = axiosData.data["messages"]
// serverMessages.forEach(function(msg){
//   let idCounter = 3
//
//   const someData = {
//     id: idCounter++,
//     content:
//     msg["message"],
//     date: "5:00 pm",
//     state: "read",
//     sender: {
//       id: 1,
//       firstName: "Dawn",
//       lastName: "Sabrina",
//       lastSeen: new Date(),
//       email: "sabrina@gmail.com",
//       avatar:
//         "https://images.unsplash.com/photo-1494790108377-be9c29b29330?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=387&q=80",
//     }
//
//   }
//   conversations[3].messages.push(someData);
// })


export default {
  defaultSettings,
  archive,
  conversations,
  notifications,
  calls,
  activeCall,
  user,
} as const;
