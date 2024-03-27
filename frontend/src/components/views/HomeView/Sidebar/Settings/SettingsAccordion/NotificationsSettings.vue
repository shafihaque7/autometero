<script setup lang="ts">
import useStore from "@src/store/store";

import AccordionButton from "@src/components/ui/data-display/AccordionButton.vue";
import Collapse from "@src/components/ui/utils/Collapse.vue";
import SettingsSwitch from "@src/components/views/HomeView/Sidebar/Settings/SettingsAccordion/SettingsSwitch.vue";
import Typography from "@src/components/ui/data-display/Typography.vue";
import Button from "@src/components/ui/inputs/Button.vue";

const props = defineProps<{
  collapsed: boolean;
  handleToggle: () => void;
}>();

const store = useStore();

import { initializeApp } from "firebase/app";
import { getMessaging, getToken, onMessage } from "firebase/messaging";
// import Button from "@src/components/ui/inputs/Button.vue";
import axios from "axios";





console.log("Notification settings")


const messaging = getMessaging();


const requestPermission = () => {
  console.log("Requesting permission...")
  Notification.requestPermission().then((permission) => {
    if (permission === 'granted') {
      console.log("Permission granted")

      getToken(messaging, { vapidKey: 'BPSCfFSbBnxGp_5BcJfO5nl4gnlf3bzweImAlk0Q1UhmYAB-1EP4IEidL5cOa99Ulmsg23868xkeejDWiInBrtc' }).then((currentToken) => {
        if (currentToken) {
          // Send the token to your server and update the UI if necessary
          console.log("Token is:",currentToken);
          axios.post('https://hingeauto.co/storeNotificationToken', {
            token: currentToken
          })
            .then(function (response) {
              console.log(response);
            })
            .catch(function (error) {
              console.log(error);
            });
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

const testNotification = async() => {
  const axiosData = await axios.post("http://127.0.0.1:8080/testNotification", {})
}



</script>

<template>
  <!--notifications settings-->
  <AccordionButton
    id="notifications-settings-toggler"
    class="w-full flex px-5 py-6 mb-3 rounded focus:outline-none"
    :collapsed="props.collapsed"
    chevron
    aria-controls="notifications-settings-collapse"
    @click="props.handleToggle()"
  >
    <Typography variant="heading-2" class="mb-4"> Notifications </Typography>
    <Typography variant="body-2"> Customize notifications </Typography>
  </AccordionButton>



  <Collapse id="notifications-settings-collapse" :collapsed="props.collapsed">

    <Button class="w-full py-4" @click="requestPermission">
      Request Notification Permission
    </Button>
    <br>

    <Button class="w-full py-4" @click="testNotification">
      Test Notification
    </Button>
    <br>

    <SettingsSwitch
      title="Allow Notifications"
      description="Receive Notifications from avian"
      :value="!!store.settings.allowNotifications"
      :handle-toggle-switch="
        (value) => (store.settings.allowNotifications = value)
      "
      class="mb-7"
    />
    <SettingsSwitch
      title="Keep Notifications"
      description="Save notifications after they are received"
      :value="!!store.settings.keepNotifications"
      :handle-toggle-switch="
        (value) => (store.settings.keepNotifications = value)
      "
      class="mb-7"
    />
  </Collapse>
</template>
