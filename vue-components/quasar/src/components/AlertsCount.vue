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
  <q-btn flat dense round icon="notifications" @click="onClick">
    <q-badge v-if="nAlerts > 0" floating color="red">
      {{ nAlerts }}
    </q-badge>
  </q-btn>
</template>
