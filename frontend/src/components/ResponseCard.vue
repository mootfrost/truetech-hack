<script setup lang="ts">
import type Suggestion from "../Suggestion.ts";

defineProps<{ suggestion: Suggestion }>()

</script>

<template>
  <span><strong>Причина обращения: </strong>{{suggestion.intent}}</span><br>
  <span><strong>Эмоция: </strong>{{suggestion.emotion}} ({{suggestion.emotion_force}})</span><br>
  <span><strong>Рекомендуемое решение: </strong>{{suggestion.answer}}</span><br><br><br><br><br><br>

  <p><strong>Возможный способ улучшения решения: </strong>{{suggestion.qa}}</p><br><br>
</template>

<style scoped>

</style>