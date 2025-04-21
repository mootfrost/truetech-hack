<script setup lang="ts">
import type Suggestion from "../Suggestion.ts";

defineProps<{ suggestion: Suggestion }>()

</script>

<template>
  <span><strong>Причина обращения: </strong>{{suggestion.intent}}</span><br>
  <span><strong>Эмоция: </strong>{{suggestion.emotion}} ({{suggestion.emotion_force}})</span><br>
  <span><strong>Рекомендуемое решение: </strong>{{suggestion.answer}}</span>
</template>

<style scoped>

</style>