<script setup lang="ts">
import type { IConversation, IMessage } from "@src/types";
import type { Ref } from "vue";
import { inject, onMounted, ref } from "vue";
import axios from "axios"

import useStore from "@src/store/store";

import Message from "@src/components/views/HomeView/Chat/ChatMiddle/Message/Message.vue";
import TimelineDivider from "@src/components/views/HomeView/Chat/ChatMiddle/TimelineDivider.vue";
import Typography from "@src/components/ui/data-display/Typography.vue";
import { getConversationObjectId } from "@src/utils";

const props = defineProps<{
  handleSelectMessage: (messageId: number) => void;
  handleDeselectMessage: (messageId: number) => void;
  selectedMessages: number[];
}>();

const store = useStore();

const aiMessages = ref([])

const container: Ref<HTMLElement | null> = ref(null);

const activeConversation = <IConversation>inject("activeConversation");

// checks whether the previous message was sent by the same user.
const isFollowUp = (index: number, previousIndex: number): boolean => {
  if (previousIndex < 0) {
    return false;
  } else {
    let previousSender = activeConversation.messages[previousIndex].sender.id;
    let currentSender = activeConversation.messages[index].sender.id;
    return previousSender === currentSender;
  }
};

// checks whether the message is sent by the authenticated user.
const isSelf = (message: IMessage): boolean => {
  return Boolean(store.user && message.sender.id === store.user.id);
};

// checks wether the new message has been sent in a new day or not.
const renderDivider = (index: number, previousIndex: number): boolean => {
  if (index === 3) {
    return true;
  } else {
    return false;
  }
};

const loadAIData = async () => {

  const conversationObjectId = getConversationObjectId(activeConversation.id)
  if (conversationObjectId !== undefined) {
    console.log("conversation object id is", conversationObjectId)

    // const axiosData = await axios.get("http://104.42.212.81:8080/ai/user/" + conversationObjectId)
    const axiosData = await axios.get("http://127.0.0.1:8080/ai/user/" + conversationObjectId)
    // console.log(axiosData.data)


    aiMessages.value = axiosData.data["aiMessages"]

    activeConversation.draftMessage = axiosData.data["aiMessageToSend"]

    console.log(aiMessages.value)
  }
}

const changeDraftMessage = (aimsg:string) => {
  activeConversation.draftMessage = aimsg
  // console.log(aimsg)
  console.log("active conversation, ",activeConversation)

}

// scroll messages to bottom.
onMounted(() => {
  (container.value as HTMLElement).scrollTop = (
    container.value as HTMLElement
  ).scrollHeight;

  loadAIData()

});
</script>

<template>
  <div
    ref="container"
    class="grow px-5 py-5 flex flex-col overflow-y-scroll scrollbar-hidden"
  >
    <div
      v-if="store.status !== 'loading'"
      v-for="(message, index) in activeConversation.messages"
      :key="index"
    >
      <TimelineDivider v-if="renderDivider(index, index - 1)" />

      <Message
        :message="message"
        :self="isSelf(message)"
        :follow-up="isFollowUp(index, index - 1)"
        :divider="renderDivider(index, index - 1)"
        :selected="props.selectedMessages.includes(message.id)"
        :handle-select-message="handleSelectMessage"
        :handle-deselect-message="handleDeselectMessage"
      />
    </div>

    <div class="w-full my-7 flex items-center justify-center">
      <div
        class="w-full h-0 border-t border-dashed dark:border-gray-600 dark:bg-opacity-0"
      ></div>

      <Typography variant="body-4" class="mx-5"> AI Message Previews </Typography>

      <div
        class="w-full h-0 border-t border-dashed dark:border-gray-600 dark:bg-opacity-0"
      ></div>
    </div>


    <div v-for="aimsg in aiMessages">
     <div class="xs:mb-6 md:mb-5 flex justify-end">


      <button @click="changeDraftMessage(aimsg)" class="block p-6 mb-6 bg-white border border-gray-200 rounded-lg shadow-md dark:bg-gray-800 dark:hover:bg-gray-700 hover:bg-gray-100 dark:border-gray-700 lg:mb-0">
         <p class="font-normal text-gray-700 dark:text-gray-400">{{ aimsg}}</p>
       </button>

    </div>

     </div>




  </div>
</template>
