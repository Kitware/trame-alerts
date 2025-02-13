<script setup lang="ts">
import { computed } from "vue";

import type { Alert } from "@/types";

interface Props {
  alerts: Alert[];
}

type Events = {
  click: [];
};

const props = defineProps<Props>();

const emit = defineEmits<Events>();

const nAlerts = computed(() => props.alerts.length);

function onClick() {
  emit("click");
}
</script>

<template>
  <v-btn @click="onClick" stacked rounded>
    <v-badge v-if="nAlerts > 0" color="error" :content="nAlerts">
      <v-icon>mdi-bell-outline</v-icon>
    </v-badge>
    <v-icon v-else>mdi-bell-outline</v-icon>
  </v-btn>
</template>
