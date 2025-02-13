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
  <div class="alert-popup-container">
    <v-slide-y-reverse-transition group>
      <v-alert
        v-for="alert in alerts"
        :key="alert.id"
        model-value="true"
        :type="alert.type"
        :title="alert.title"
        :text="alert.text"
        density="compact"
      >
        <template #close>
          <v-btn @click="onRemove(alert.id)"></v-btn>
        </template>
      </v-alert>
    </v-slide-y-reverse-transition>
  </div>
</template>

<style>
.alert-popup-container {
  position: fixed;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 100%;
  max-width: 40em;
  display: grid;
  grid-gap: 0.5em;
  z-index: 999;
  padding: 0.5em;
}
</style>
