<script setup lang="ts">
import type { Alert } from "@/types";

interface Props {
  alerts: Alert[];
}

type Events = {
  remove: [id: number];
};

defineProps<Props>();

const emit = defineEmits<Events>();

function onRemove(id: number) {
  emit("remove", id);
}
</script>

<template>
  <div class="alert-list-container">
    <v-alert
      v-for="alert of alerts"
      :key="alert.id"
      model-value="true"
      :type="alert.type"
      :title="alert.title"
      density="compact"
      variant="tonal"
    >
      <template #text>
        <div class="alert-list-text">{{ alert.text }}</div>
      </template>

      <template #close>
        <v-btn @click="onRemove(alert.id)"></v-btn>
      </template>
    </v-alert>
  </div>
</template>

<style>
.alert-list-container {
  display: grid;
  grid-gap: 0.25em;
}

.alert-list-text {
  white-space: pre-wrap;
}
</style>
