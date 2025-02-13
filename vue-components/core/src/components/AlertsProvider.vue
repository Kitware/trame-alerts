<script setup lang="ts">
import { computed } from "vue";
import type {
  Alert,
  AlertConstructor,
  AlertConstructorSpecialized,
} from "@/types";

type SlotPropsNames = {
  alerts: string;
  allAlerts: string;
  activeAlerts: string;
  elapsedAlerts: string;
  createAlert: string;
  createSuccessAlert: string;
  createWarningAlert: string;
  createErrorAlert: string;
  createInfoAlert: string;
  dismissAlert: string;
  removeAlert: string;
  clearAlerts: string;
};

interface Props {
  alerts: { [id: number]: Alert };
  slotPropsNames: SlotPropsNames;
}

type Events = {
  onCreateAlert: [alert: AlertConstructor];
  onCreateSuccessAlert: [alert: AlertConstructorSpecialized];
  onCreateWarningAlert: [alert: AlertConstructorSpecialized];
  onCreateErrorAlert: [alert: AlertConstructorSpecialized];
  onCreateInfoAlert: [alert: AlertConstructorSpecialized];
  onDismissAlert: [id: number];
  onRemoveAlert: [id: number];
  onClearAlerts: [];
};

const props = defineProps<Props>();

const emit = defineEmits<Events>();

const allAlerts = computed(() => {
  return Object.values(props.alerts);
});

const activeAlerts = computed(() => {
  return allAlerts.value.filter((alert) => !alert.elapsed);
});

const elapsedAlerts = computed(() => {
  return allAlerts.value.filter((alert) => alert.elapsed);
});

function removeAlert(id: number) {
  emit("onRemoveAlert", id);
}

function dismissAlert(id: number) {
  emit("onDismissAlert", id);
}

function createAlert(alert: AlertConstructor) {
  emit("onCreateAlert", alert);
}

function createSuccessAlert(alert: AlertConstructorSpecialized) {
  emit("onCreateSuccessAlert", alert);
}

function createWarningAlert(alert: AlertConstructorSpecialized) {
  emit("onCreateWarningAlert", alert);
}

function createErrorAlert(alert: AlertConstructorSpecialized) {
  emit("onCreateErrorAlert", alert);
}

function createInfoAlert(alert: AlertConstructorSpecialized) {
  emit("onCreateInfoAlert", alert);
}

function clearAlerts() {
  emit("onClearAlerts");
}
</script>

<template>
  <slot
    :[slotPropsNames.alerts]="alerts"
    :[slotPropsNames.allAlerts]="allAlerts"
    :[slotPropsNames.activeAlerts]="activeAlerts"
    :[slotPropsNames.elapsedAlerts]="elapsedAlerts"
    :[slotPropsNames.createAlert]="createAlert"
    :[slotPropsNames.createSuccessAlert]="createSuccessAlert"
    :[slotPropsNames.createWarningAlert]="createWarningAlert"
    :[slotPropsNames.createErrorAlert]="createErrorAlert"
    :[slotPropsNames.createInfoAlert]="createInfoAlert"
    :[slotPropsNames.removeAlert]="removeAlert"
    :[slotPropsNames.dismissAlert]="dismissAlert"
    :[slotPropsNames.clearAlerts]="clearAlerts"
  ></slot>
</template>
