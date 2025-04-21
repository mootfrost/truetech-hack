<template>
  <button
      :style="{ backgroundColor: currentSender === Sender.Operator ? '#4caf50' : '#2196f3', color: 'white', padding: '10px 20px', border: 'none', borderRadius: '5px' }"
      @click="toggleSender"
      type="button"
  >
    {{ currentSender }}
  </button>
</template>

<script lang="ts" setup>
import { ref, defineEmits } from 'vue';
import {Sender} from "../Sender.ts";



const emit = defineEmits<{
  (e: 'update', value: Sender): void;
}>();

const currentSender = ref<Sender>(Sender.Client );

function toggleSender() {
  currentSender.value =
      currentSender.value === Sender.Operator ? Sender.Client : Sender.Operator;
  emit('update', currentSender.value);
}
</script>
