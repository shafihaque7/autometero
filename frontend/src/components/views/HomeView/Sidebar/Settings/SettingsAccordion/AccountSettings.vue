<script setup lang="ts">
import { onMounted, ref } from "vue";
import type { Ref } from "vue";

import useStore from "@src/store/store";

import AccordionButton from "@src/components/ui/data-display/AccordionButton.vue";
import Typography from "@src/components/ui/data-display/Typography.vue";
import Collapse from "@src/components/ui/utils/Collapse.vue";
import TextInput from "@src/components/ui/inputs/TextInput.vue";
import DropFileUpload from "@src/components/ui/inputs/DropFileUpload.vue";
import Button from "@src/components/ui/inputs/Button.vue";
import axios from "axios";
import Textarea from "@src/components/ui/inputs/Textarea.vue";

// Types
interface AccountValues {
  firstName: string | undefined;
  lastName: string | undefined;
  avatar: File | undefined;
}

// Variables
const props = defineProps<{
  collapsed: boolean;
  handleToggle: () => void;
}>();

const store = useStore();

const accountValues: Ref<AccountValues> = ref({
  firstName: store.user?.firstName,
  lastName: store.user?.lastName,
  avatar: undefined,
});

const loading = ref(false);

// (event) handle submitting the values of the form.
const handleSubmit = async () => {
  loading.value = true;

  const axiosData = await axios.post("http://104.42.212.81:8080/ai/updatePrompt", {
    "updatedPrompt": chatgptPrompt.value,
  })


  console.log(chatgptPrompt.value)

  loading.value = false
};
const lastUpdatedDateAndTime = ref("")
const chatgptPrompt = ref("")

const loadLastUpdated = async () => {
  const axiosData = await axios.get("http://104.42.212.81:8080/getLastUpdated")
  let lastUpdatedString = axiosData.data["lastUpdatedTimeForScraper"]


  if (axiosData.data["currentlyRunning"] == true) {
    lastUpdatedString += " (Currenly Running)"
    loading.value = true
  }
  // console.log(axiosData.data)
  lastUpdatedDateAndTime.value = lastUpdatedString
  chatgptPrompt.value = axiosData.data["chatgptPrompt"]
}

const runAutoScraper = async () => {
  console.log("Running autoscraper")
  loading.value = true
  const axiosData = await axios.post("http://104.42.212.81:8080/runautoscraper", {})
  loading.value = false
  lastUpdatedDateAndTime.value = axiosData.data["lastUpdatedTimeForScraper"]


}

onMounted(() => {
  loadLastUpdated()
});

</script>

<template>
  <!--account settings-->
  <Typography variant="heading-2" class="mb-4"> Last ran: {{ lastUpdatedDateAndTime }}</Typography>

  <Button class="w-full py-4" :loading="loading" @click="runAutoScraper">
    Run Autoscraper
  </Button>

  <AccordionButton
    id="account-settings-toggler"
    class="w-full flex px-5 py-6 mb-3 rounded focus:outline-none"
    :collapsed="props.collapsed"
    chevron
    aria-controls="account-settings-collapse"
    @click="handleToggle()"
  >
    <Typography variant="heading-2" class="mb-4"> AI Settings </Typography>
    <Typography variant="body-2"> Update your AI prompt</Typography>
  </AccordionButton>

  <Collapse id="account-settings-collapse" :collapsed="props.collapsed">
    <Textarea
      rows="8"
      label="Current Chatgpt prompt"
      class="mb-7"
      :value="chatgptPrompt"
      v-model="chatgptPrompt"
      @value-changed="(value) => (accountValues.firstName = value)"
    />

<!--    <TextInput-->
<!--      label="First name"-->
<!--      class="mb-7"-->
<!--      :value="accountValues?.firstName"-->
<!--      @value-changed="(value) => (accountValues.firstName = value)"-->
<!--    />-->
<!--    <TextInput-->
<!--      label="Last name"-->
<!--      class="mb-7"-->
<!--      :value="accountValues?.lastName"-->
<!--      @value-changed="(value) => (accountValues.lastName = value)"-->
<!--    />-->
<!--    <DropFileUpload-->
<!--      label="Avatar"-->
<!--      class="mb-7"-->
<!--      accept="image/*"-->
<!--      :value="accountValues.avatar"-->
<!--      @value-changed="(value) => (accountValues.avatar = value)"-->
<!--    />-->
    <Button class="w-full py-4" @click="handleSubmit" :loading="loading">
      Save Settings
    </Button>
  </Collapse>
</template>
