<script setup lang="ts">
import { watch, onMounted } from "vue";

import { useQuasar } from "quasar";

import type { Alert } from "@/types";

const MAX_ALERT_TEXT_LENGTH = 80;

interface Props {
  alerts: Alert[];
}

type Events = {
  remove: [id: number];
};

function alertToNotifyType(alert: Alert) {
  if (alert.type === "error") {
    return "negative";
  } else if (alert.type === "success") {
    return "positive";
  } else if (alert.type === "warning") {
    return "warning";
  } else {
    return "info";
  }
}

const props = defineProps<Props>();

const emit = defineEmits<Events>();

let dismissMap: { [id: number]: () => void } = {};

function onRemove(id: number) {
  emit("remove", id);
}

const $q = useQuasar();

function updateAlerts(alerts: Alert[]) {
  const newDismissMap: { [id: number]: () => void } = {};

  // Add notification for any new alerts
  alerts.forEach((alert) => {
    if (dismissMap[alert.id] !== undefined) {
      // Alert was seen before
      newDismissMap[alert.id] = dismissMap[alert.id];
    } else {
      // First time seeing this alert
      newDismissMap[alert.id] = $q.notify({
        message: alert.title,
        caption:
          alert.text.length > MAX_ALERT_TEXT_LENGTH
            ? alert.text.slice(0, MAX_ALERT_TEXT_LENGTH) + "..."
            : alert.text,
        type: alertToNotifyType(alert),
        group: false,
        timeout: 0,
        actions: [
          {
            icon: "close",
            "aria-label": "Dismiss",
            color: "white",
            noDismiss: true,
            handler: () => onRemove(alert.id),
          },
        ],
      });
    }
  });

  // Remove notification for any alerts that disappeared
  Object.entries(dismissMap).forEach(([id, dismissFn]) => {
    if (newDismissMap[id as any] === undefined) {
      dismissFn();
    }
  });

  dismissMap = newDismissMap;
}

watch(
  () => props.alerts,
  (newValue) => {
    updateAlerts(newValue);
  }
);

onMounted(() => {
  updateAlerts(props.alerts);
});
</script>
