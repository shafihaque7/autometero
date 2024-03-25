<script setup lang="ts">
import { ref, onMounted, onUnmounted } from "vue";


import useStore from "@src/store/store";
import { fetchData } from "@src/store/defaults";

import FadeTransition from "@src/components/ui/transitions/FadeTransition.vue";

// Fixes
// todo fix clicking back to close conversations.

// future features:
// todo add video calling
// todo add stories

// Refactoring code:
// todo reorganize component structure
// todo rerfactor make everything that can be a ui component into one.
// todo refactor remove getters from utils file and add them to store folder.
// todo improve the video component.

// Accessability:
// todo improve the way you view messages.
// todo make multi-select more accessible.
// todo make dropdown menus more accessible.
// todo make modals more accessible.
// todo make lists (i.e conversations, contacts, calls) more accessible.

// SEO.
// todo improve seo.

// Performance:
// todo add dynamic imports.
// todo add chunking.

import { initializeApp } from "firebase/app";
import { getMessaging, getToken, onMessage } from "firebase/messaging";
import Button from "@src/components/ui/inputs/Button.vue";

const firebaseConfig = {
  apiKey: "AIzaSyC17NBzSzPZVUd8PZY0jmtWHLB5pppSyOg",
  authDomain: "hingeautomation.firebaseapp.com",
  projectId: "hingeautomation",
  storageBucket: "hingeautomation.appspot.com",
  messagingSenderId: "968993586795",
  appId: "1:968993586795:web:25aaed34307fc3cccf3b2e",
  measurementId: "G-65GDBLHRQY"
};


const app = initializeApp(firebaseConfig);


// Get registration token. Initially this makes a network call, once retrieved
// subsequent calls to getToken will return from cache.
const messaging = getMessaging();
onMessage(messaging, (payload) => {
  console.log('Message received. ', payload);
  // ...
});

getToken(messaging, { vapidKey: 'BPSCfFSbBnxGp_5BcJfO5nl4gnlf3bzweImAlk0Q1UhmYAB-1EP4IEidL5cOa99Ulmsg23868xkeejDWiInBrtc' }).then((currentToken) => {
  if (currentToken) {
    // Send the token to your server and update the UI if necessary
    console.log("Token is:",currentToken);
    // ...
  } else {
    // Show permission request UI
    console.log('No registration token available. Request permission to generate one.');
    // ...
  }
}).catch((err) => {
  console.log('An error occurred while retrieving token. ', err);
  // ...
});


const requestPermission = () => {
  console.log("Requesting permission...")
  Notification.requestPermission().then((permission) => {
    if (permission === 'granted') {
      console.log("Permission granted")

      getToken(messaging, { vapidKey: 'BPSCfFSbBnxGp_5BcJfO5nl4gnlf3bzweImAlk0Q1UhmYAB-1EP4IEidL5cOa99Ulmsg23868xkeejDWiInBrtc' }).then((currentToken) => {
        if (currentToken) {
          // Send the token to your server and update the UI if necessary
          console.log("Token is:",currentToken);
          // ...
        } else {
          // Show permission request UI
          console.log('No registration token available. Request permission to generate one.');
          // ...
        }
      }).catch((err) => {
        console.log('An error occurred while retrieving token. ', err);
        // ...
      });


    }
    else {
      console.log("Permission not granted")
    }
  } )

}



const store = useStore();

// update localStorage with state changes
store.$subscribe((_mutation, state) => {
  localStorage.setItem("chat", JSON.stringify(state));
});

// here we load the data from the server.
onMounted(async () => {
  store.status = "loading";

  // fake server call
  setTimeout(() => {
    store.delayLoading = false;
  });
  const request = await fetchData();

  store.$patch({
    status: "success",
    user: request.data.user,
    conversations: request.data.conversations,
    notifications: request.data.notifications,
    archivedConversations: request.data.archivedConversations,
  });
});

// the app height
const height = ref(`${window.innerHeight}px`);

// change the app height to the window hight.
const resizeWindow = () => {
  height.value = `${window.innerHeight}px`;
};

// and add the resize event when the component mounts.
onMounted(() => {
  window.addEventListener("resize", resizeWindow);
});

// remove the event when un-mounting the component.
onUnmounted(() => {
  window.removeEventListener("resize", resizeWindow);
});
</script>

<template>
  <div :class="{ dark: store.settings.darkMode }">
    <div
      class="bg-white dark:bg-gray-800 transition-colors duration-500"
      :style="{ height: height }"
    >

      <Button class="w-full py-4" @click="requestPermission">
        Allow Notification
      </Button>
      <router-view v-slot="{ Component }">
        <FadeTransition>
          <component :is="Component" />
        </FadeTransition>
      </router-view>
    </div>
  </div>
</template>
