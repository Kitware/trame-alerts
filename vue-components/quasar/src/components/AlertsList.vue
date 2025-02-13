<script setup lang="ts">
import type { Alert } from "@/types";

interface Props {
  alerts: Alert[];
}

type Events = {
  remove: [id: number];
};

function alertIcon(alert: Alert) {
  if (alert.type === "error") {
    return "warning";
  } else if (alert.type === "success") {
    return "check_circle";
  } else if (alert.type === "warning") {
    return "error";
  } else {
    return "info";
  }
}

function alertColor(alert: Alert) {
  if (alert.type === "error") {
    return "negative";
  } else if (alert.type === "success") {
    return "positive";
  } else if (alert.type === "warning") {
    return "warning";
  } else {
    return "grey";
  }
}

function alertBackground(alert: Alert) {
  if (alert.type === "error") {
    return "bg-red-1";
  } else if (alert.type === "success") {
    return "bg-green-1";
  } else if (alert.type === "warning") {
    return "bg-orange-1";
  } else {
    return "bg-grey-1";
  }
}

defineProps<Props>();

const emit = defineEmits<Events>();

function onRemove(id: number) {
  emit("remove", id);
}
</script>

<template>
  <q-list bordered separator class="rounded-borders">
    <template v-for="alert in alerts" :key="alert.id">
      <q-item :class="alertBackground(alert)">
        <q-item-section avatar>
          <q-icon :name="alertIcon(alert)" :color="alertColor(alert)" />
        </q-item-section>

        <q-item-section>
          <q-item-label lines="1">{{ alert.title }}</q-item-label>
          <q-item-label caption>{{ alert.text }}</q-item-label>
        </q-item-section>

        <q-item-section side>
          <q-btn
            flat
            round
            size="sm"
            icon="close"
            @click="() => onRemove(alert.id)"
          />
        </q-item-section>
      </q-item>
    </template>
  </q-list>
</template>
