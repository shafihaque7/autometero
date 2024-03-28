<script setup lang="ts">
import type { IMessage, INotification } from "@src/types";
import axios from "axios"
import Typography from "@src/components/ui/data-display/Typography.vue";
import { computed } from "vue";
import VueCountdown from '@chenfengyuan/vue-countdown';

import {
  ArrowPathIcon,
  LockClosedIcon,
  PlusCircleIcon,
} from "@heroicons/vue/24/outline";
import useStore from "@src/store/store";
import { getConversationIdFromObjectId, getConversationIndex } from "@src/utils";

const props = defineProps<{
  notification: INotification;
}>();

const store = useStore();



const changeSelectedConversation = async () => {
  console.log("fsdfds",props.notification.objectId)
  const conversationId = getConversationIdFromObjectId(props.notification.objectId)
  if (conversationId != null) {
    const conversationIndex = getConversationIndex(conversationId);

    if (conversationIndex != null) {
      const axiosData = await axios.get("https://hingeauto.co/user/" + props.notification.objectId)
      const serverMessages = axiosData.data["messages"]
      console.log(serverMessages)
      const allMessages: IMessage[] = []
      serverMessages.forEach(function(msg: any) {
        let idCounter = 3

        const someData = {
          id: idCounter++,
          content:
            msg["message"],
          date: "5:00 pm",
          state: "read",
          sender: {
            id: (msg["user"] == "You") ? 1 : 45454,
            firstName: "Dawn",
            lastName: "Sabrina",
            lastSeen: new Date(),
            email: "sabrina@gmail.com",
            avatar:
              "https://images.unsplash.com/photo-1494790108377-be9c29b29330?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=387&q=80",
          }

        }

        allMessages.push(someData)

      })
      console.log("allmesgsgsg froms message", allMessages)
      store.conversations[conversationIndex].messages = allMessages


      // Figure this shit out it doesn't make sense
      store.activeConversationId = conversationId + 1;
      store.conversationOpen = "open";
    }
  }


  // props.handleConversationChange(3);
}
</script>

<template>
  <div
    class="w-full px-5 py-5 mb-3 flex rounded outline-none"
    tabindex="0"
    :aria-label="props.notification.message"
  >
    <!--notifications icon-->
    <div class="mr-4">
      <div
        class="w-7 h-7 flex justify-center items-center rounded-full transition duration-500"
        :class="{
          'bg-blue-100 dark:bg-blue-600':
            notification.flag === 'account-update',
          'bg-yellow-100 dark:bg-yellow-600': notification.flag === 'security',
          'bg-green-100 dark:bg-green-600':
            notification.flag === 'added-to-group',
        }"
      >
        <ArrowPathIcon
          v-if="notification.flag === 'account-update'"
          class="w-5 h-5 stroke-1 text-blue-500 dark:text-white transition duration-500"
        />
        <LockClosedIcon
          v-else-if="notification.flag === 'security'"
          class="w-5 h-5 stroke-1 text-yellow-500 dark:text-white transition duration-500"
        />
        <PlusCircleIcon
          v-else-if="notification.flag === 'added-to-group'"
          class="w-5 h-5 stroke-1 text-green-500 dark:text-white transition duration-500"
        />
      </div>
    </div>

    <!--notification content-->

    <div class="grow" @click="changeSelectedConversation">
      <Typography variant="heading-2" class="mb-4">
        {{ props.notification.title }}
        <vue-countdown :time="props.notification.sendTime * 60 * 60 * 1000" v-slot="{ hours, minutes, seconds }">
          {{ hours }} hours, {{ minutes }} minutes, {{ seconds }} seconds.
        </vue-countdown>

      </Typography>

      <Typography variant="body-2">
        {{ props.notification.message }}
<!--        {{ props.notification.sendTime}}-->
      </Typography>
    </div>
  </div>
</template>
