<script setup lang="ts">
import type { IConversation, IMessage } from "@src/types";

import { activeCall } from "@src/store/defaults";
import useStore from "@src/store/store";
import { getAvatar, getConversationObjectId, getName } from "@src/utils";
import { inject, ref } from "vue";

import {
  ChevronLeftIcon,
  EllipsisVerticalIcon,
  InformationCircleIcon,
  MagnifyingGlassIcon,
  NoSymbolIcon,
  PhoneIcon,
  ShareIcon,
  ArrowPathIcon,

} from "@heroicons/vue/24/outline";
import Typography from "@src/components/ui/data-display/Typography.vue";
import IconButton from "@src/components/ui/inputs/IconButton.vue";
import Dropdown from "@src/components/ui/navigation/Dropdown/Dropdown.vue";
import DropdownLink from "@src/components/ui/navigation/Dropdown/DropdownLink.vue";
import axios from "axios";

const props = defineProps<{
  handleOpenInfo: () => void;
  handleOpenSearch: () => void;
}>();

const store = useStore();

const activeConversation = <IConversation>inject("activeConversation");

const showDropdown = ref(false);

// (event) close dropdown menu when click item
const handleCloseDropdown = () => {
  showDropdown.value = false;
};

// (event) close dropdown menu when clicking outside the menu.
const handleClickOutside = (event: Event) => {
  let target = event.target as HTMLElement;
  let parentElement = target.parentElement as HTMLElement;

  if (
    target &&
    !(target.classList as Element["classList"]).contains("open-top-menu") &&
    parentElement &&
    !(parentElement.classList as Element["classList"]).contains("open-top-menu")
  ) {
    handleCloseDropdown();
  }
};

// (event) close the selected conversation
const handleCloseConversation = () => {
  store.conversationOpen = "close";
  store.activeConversationId = null;
};

// (event) open the voice call modal and expand call
const handleOpenVoiceCallModal = () => {
  store.activeCall = activeCall;
  store.callMinimized = false;

  // wait for the transition to ongoing status to end
  setTimeout(() => {
    store.openVoiceCall = true;
  }, 300);
};

const reloadConversation = async () => {
  console.log("Reload conversation called")
  // console.log("current active conversation", activeConversation)
  // activeConversation.messages[0].content = "Checking if changed work"

  const conversationObjectId = getConversationObjectId(activeConversation.id)
  const axiosData = await axios.post("https://hingeauto.co/appium/refreshUserMessage", {
    "userId": conversationObjectId
  })

  const allMessages: IMessage[] = []

  const serverMessages = axiosData.data
  serverMessages.forEach(function(msg: any){
    let idCounter = 3

    const someData = {
      id: idCounter++,
      content:
        msg["message"],
      date: "5:30 pm",
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

  activeConversation.messages = allMessages
}

const refreshAiData = async () => {

  const conversationObjectId = getConversationObjectId(activeConversation.id)
  if (conversationObjectId !== undefined) {
    console.log("conversation object id is", conversationObjectId)

    const axiosData = await axios.get("https://hingeauto.co/ai/refreshmessages/" + conversationObjectId)
    // const axiosData = await axios.get("http://127.0.0.1:8080/ai/user/" + conversationObjectId)
    // console.log(axiosData.data)

    const allAiMessages: IMessage[] = []

    const dataAiMessages = axiosData.data["aiMessages"]

    let idNumberiMessage = 20

    dataAiMessages.forEach(function(aiMsg: string){
      const aiImessage: IMessage = {
        id: idNumberiMessage,
        content: aiMsg,
        date: "",
        state: "read",
        sender: {
          id: 1,
          firstName: "Dawn",
          lastName: "Sabrina",
          lastSeen: new Date(),
          email: "sabrina@gmail.com",
          avatar: "https://images.unsplash.com/photo-1494790108377-be9c29b29330?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=387&q=80",
        }
      }
      allAiMessages.push(aiImessage)
    })

    // aiMessages.value = axiosData.data["aiMessages"]

    activeConversation.aiMessages = allAiMessages



    activeConversation.draftMessage = axiosData.data["aiMessageToSend"]

  }
}


</script>

<template>
  <!--conversation info-->
  <div class="w-full flex justify-center items-center">
    <div class="group mr-4 md:hidden">
      <IconButton
        class="w-7 h-7"
        @click="handleCloseConversation"
        title="close conversation"
        aria-label=""
      >
        <ChevronLeftIcon
          aria-label="close conversation"
          class="w-[1.25rem] h-[1.25rem] text-gray-300 group-hover:text-indigo-300"
        />
      </IconButton>
    </div>

    <div v-if="store.status !== 'loading'" class="flex grow">
      <!--avatar-->
      <button
        class="mr-5 outline-none"
        @click="props.handleOpenInfo"
        aria-label="profile avatar"
      >
        <div
          :style="{
            backgroundImage: `url(${getAvatar(activeConversation)})`,
          }"
          class="w-[2.25rem] h-[2.25rem] rounded-full bg-cover bg-center"
        ></div>
      </button>

      <!--name and last seen-->
      <div class="flex flex-col">
        <Typography
          variant="heading-2"
          @click="props.handleOpenInfo"
          class="mb-2 default-outline cursor-pointer"
          tabindex="0"
        >
          {{ getName(activeConversation) }}
        </Typography>

        <Typography
          variant="body-2"
          class="font-extralight default-outline rounded-[.25rem]"
          tabindex="0"
          aria-label="Last seen december 16, 2019"
        >
          Last seen Feb 22, 2024
        </Typography>
      </div>
    </div>

    <div class="flex" :class="{ hidden: store.status === 'loading' }">
      <IconButton
        title="refresh messages"
        aria-label="refresh messages"
        @click="refreshAiData"
        class="group w-7 h-7 mr-3"
      >
        <ArrowPathIcon
          class="w-[1.25rem] h-[1.25rem] text-gray-400 group-hover:text-indigo-300"
        />
      </IconButton>


      <!--search button-->
      <IconButton
        title="search messages"
        aria-label="search messages"
        @click="props.handleOpenSearch"
        class="group w-7 h-7 mr-3"
      >
        <MagnifyingGlassIcon
          class="w-[1.25rem] h-[1.25rem] text-gray-400 group-hover:text-indigo-300"
        />
      </IconButton>

      <div class="relative">
        <!--dropdown menu button-->
        <IconButton
          id="open-conversation-menu"
          @click="showDropdown = !showDropdown"
          tabindex="0"
          class="open-top-menu group w-7 h-7"
          :aria-expanded="showDropdown"
          aria-controls="conversation-menu"
          title="toggle conversation menu"
          aria-label="toggle conversation menu"
        >
          <EllipsisVerticalIcon
            class="open-top-menu w-[1.25rem] h-[1.25rem] text-gray-400 group-hover:text-indigo-300"
          />
        </IconButton>

        <!--dropdown menu-->
        <Dropdown
          id="conversation-menu"
          :close-dropdown="() => (showDropdown = false)"
          :show="showDropdown"
          :position="['right-0']"
          :handle-click-outside="handleClickOutside"
          aria-labelledby="open-conversation-menu"
        >

          <DropdownLink
            :handle-click="
              () => {
                handleCloseDropdown();
                reloadConversation();
                // props.handleOpenInfo();
              }
            "
          >
            <ArrowPathIcon
              class="h-5 w-5 mr-3 text-black opacity-60 dark:text-white dark:opacity-70"
            />
            Reload Conversation
          </DropdownLink>


          <DropdownLink
            :handle-click="
              () => {
                handleCloseDropdown();
                props.handleOpenInfo();
              }
            "
          >
            <InformationCircleIcon
              class="h-5 w-5 mr-3 text-black opacity-60 dark:text-white dark:opacity-70"
            />
            Profile Information
          </DropdownLink>

          <DropdownLink
            :handle-click="
              () => {
                handleCloseDropdown();
                handleOpenVoiceCallModal();
              }
            "
          >
            <PhoneIcon
              class="h-5 w-5 mr-3 text-black opacity-60 dark:text-white dark:opacity-70"
            />
            Voice call
          </DropdownLink>

          <DropdownLink :handle-click="handleCloseDropdown">
            <ShareIcon
              class="h-5 w-5 mr-3 text-black opacity-60 dark:text-white dark:opacity-70"
            />
            Shared media
          </DropdownLink>

          <DropdownLink :handle-click="handleCloseDropdown" color="danger">
            <NoSymbolIcon class="h-5 w-5 mr-3" />
            Block contact
          </DropdownLink>
        </Dropdown>
      </div>
    </div>
  </div>
</template>
