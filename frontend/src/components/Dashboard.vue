<script setup lang="ts">

import {ref} from "vue";
import type Dialog from "../Dialog.ts";
import ToggleButton from './ToggleButton.vue';
import axios from "axios";
import type Suggestion from "../Suggestion.ts";
import ResponseCard from "./ResponseCard.vue";
import HistoryCard from "./HistoryCard.vue";


const dialog = ref<Dialog>()
const disabled = ref(false)
const message = ref('')
const phone = ref('')
const client = ref()
const client_id = ref('')
const sender = ref<string>('Клиент');
const includeAIAsOperatorResponse = ref(true)
const waiting = ref(false)
const currentSuggestion = ref<Suggestion>()


async function getClientByPhone() {
  const resp = await axios.get(`/client`, {
    params: {
      phone: phone.value
    }
  })
  client.value = resp.data
}

async function getClientById() {
  const resp = await axios.get(`/client`, {
    params: {
      id: client_id.value
    }
  })
  client.value = resp.data
}

async function createDialog() {
  let data = {}
  if (client_id.value) {
    await getClientById()
    data = {client_id: client.value.id}
  }
  else if (phone.value) {
    await getClientByPhone()
    data = {client_id: client.value.id}
  }
  const resp = await axios.post('/dialog/create', data)
  dialog.value = resp.data
}

async function updateDialog(text: string) {
  const resp = await axios.post('/dialog/update', {dialog_id: dialog.value?.id, message: text})
  dialog.value = resp.data
}

async function getSuggestion() {
  const resp = await axios.post<Suggestion>('/suggest/query-agent', {question: message.value, dialog_id: dialog.value?.id})
  return resp.data
}

async function sendMessage() {
  waiting.value = true
  if (dialog.value === undefined){
    await createDialog()
  }

  disabled.value = true
  await updateDialog(sender.value + ': ' + message.value)
  const resp = await getSuggestion()
  currentSuggestion.value = resp
  if (includeAIAsOperatorResponse.value) {
    await updateDialog('Оператор: ' + resp.answer)
  }
  waiting.value = false
}

function onSenderChange(value: string) {
  sender.value = value;
}
</script>

<template>
  <div class="body">
    <div class="layout">
      <div class="left-panel">
        <h2>Результаты</h2>
        <div id="result-box" class="result-box">
          <ResponseCard :suggestion="currentSuggestion" v-if="currentSuggestion && !waiting"/>
          <span v-if="waiting">⏳ Получение ответа...</span>
        </div>
      </div>
      <div class="right-panel">
        <div class="history-section">
          <h2>История</h2> <div id="history-box" class="history-box">
          <HistoryCard v-if="dialog" v-for="el in dialog.messages"
                       :message="el"
          />
        </div>
        </div> <form class="form-panel" id="chat-form">
        <div class="input-group">
          <label for="user-input">Запрос пользователя</label>
          <input type="text" v-model="message" required />
        </div> <div class="input-group">
        <label for="phone-input">Если известен, номер телефона</label>
        <input type="text" v-model="phone" />
      </div> <div class="input-group"> <label for="id-input">или ID</label>
        <input type="text" v-model="client_id" :readonly="disabled"  /> </div>
        <div class="input-group"> <label>
          <span v-if="client" style="color:green">Диалог с клиентом: {{client.id}}. Обновите, чтобы создать новый диалог</span> <span v-if="!client && dialog" style="color:darkorange">Диалог с неизвестным клиентом. Обновите, чтобы создать новый диалог</span> <br>
          <input type="checkbox" v-model="includeAIAsOperatorResponse" /> <span>Использовать ответ ассистента, как ответ оператора</span><br><br>
          <span>Сообщение от имени:</span> <ToggleButton @update="onSenderChange" />
        </label>
        </div>
        <button type="button" @click="sendMessage">Отправить сообщение</button>
      </form>
      </div>
    </div>
  </div>
</template>

<style scoped>
@import url('https://fonts.cdnfonts.com/css/segoe-ui-4');

.body {
  margin: 0;
  padding: 0;
  font-family: Segoe UI, sans-serif !important;
  background: #f9f9f9;
  color: #333;
}

.layout {
  display: flex;
  flex-direction: row;
  height: 100vh;
}

.left-panel,
.right-panel {
  padding: 1rem;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.suggestion {
  display: block;
  color: #444;
  font-size: 0.95em;
  margin-top: 4px;
}

.left-panel {
  flex: 2;
  background: #ffffff;
  border-right: 1px solid #eee;
}
.result-box {
  font-size: 1.5em!important;
  line-height: 1.5;
}
@media (max-width: 768px) {
  .history-card {
    font-size: 1rem;
    padding: 10px 14px;
  }
}

.history-section {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}
.right-panel {
  flex: 1;
  background: #ffffff;
  display: flex;
  flex-direction: column;
  padding: 1rem;
  overflow: hidden;
}

h2 {
  margin-top: 0;
  font-size: 20px;
  margin-bottom: 1rem;
}

.form-panel {
  background: #fff;
  padding: 1rem;
  border-top: 1px solid #ddd;
  box-shadow: 0 -2px 5px rgba(0,0,0,0.05);
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.input-group {
  display: flex;
  flex-direction: column;
}

.input-group label {
  font-size: 13px;
  margin-bottom: 4px;
}

.input-group input {
  padding: 8px;
  font-size: 14px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

button[type="button"] {
  padding: 10px;
  font-size: 16px;
  background-color: #007acc;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button[type="submit"]:hover {
  background-color: #005f99;
}

input[type="text"] {
  width: 100%;
  max-width: 100%;
  box-sizing: border-box;
}
.result-box,
.history-box {
  flex: 1;
  background: #f0f0f0;
  padding: 10px;
  border-radius: 6px;
  overflow-y: auto;
  font-size: 14px;
  min-height: 0;
}

@media (max-width: 768px) {
  html, body {
    height: 100%;
    overflow: hidden;
  }

  .layout {
    display: flex;
    flex-direction: column;
    height: 100vh;
  }

  .left-panel {
    flex: none;
    width: 100%;
    height: 40vh;
    overflow-y: auto;
    padding: 1rem;
    box-sizing: border-box;
  }

  .right-panel {
    flex: none;
    width: 100%;
    height: 60vh;
    overflow: hidden;
    padding: 1rem;
    box-sizing: border-box;
    display: flex;
    flex-direction: column;
  }

  .history-box {
    flex: 1;
    overflow-y: auto;
    padding: 10px;
    background: #f0f0f0;
    border-radius: 6px;
    font-size: 14px;
    margin-bottom: 270px;
  }

  .form-panel {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    background: #fff;
    padding: 1rem;
    border-top: 1px solid #ddd;
    box-shadow: 0 -2px 6px rgba(0,0,0,0.08);
    z-index: 10;
  }

  input[type="text"],
  button[type="submit"] {
    width: 100%;
    box-sizing: border-box;
  }
}
</style>