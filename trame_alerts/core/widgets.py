from trame_client.widgets.core import AbstractElement

from trame_alerts.core.service import get_alerts_service, DEFAULT_ALERTS_KEY
from trame_alerts.core import module

__all__ = [
    "AlertsProvider",
]


class HtmlElement(AbstractElement):
    def __init__(self, _elem_name, children=None, **kwargs):
        super().__init__(_elem_name, children, **kwargs)
        if self.server:
            self.server.enable_module(module)


ALERTS_SLOT_PROP = "alerts"
ALL_ALERTS_SLOT_PROP = "allAlerts"
ACTIVE_ALERTS_SLOT_PROP = "activeAlerts"
ELAPSED_ALERTS_SLOT_PROP = "elapsedAlerts"
CREATE_ALERT_SLOT_PROP = "createAlert"
CREATE_SUCCESS_ALERT_SLOT_PROP = "createSuccessAlert"
CREATE_WARNING_ALERT_SLOT_PROP = "createWarningAlert"
CREATE_ERROR_ALERT_SLOT_PROP = "createErrorAlert"
CREATE_INFO_ALERT_SLOT_PROP = "createInfoAlert"
DISMISS_ALERT_SLOT_PROP = "dismissAlert"
REMOVE_ALERT_SLOT_PROP = "removeAlert"
CLEAR_ALERTS_SLOT_PROP = "clearAlerts"


class AlertsProvider(HtmlElement):
    """Widget that connects to an AlertService and provides its descendents with alerts data.

    When placing an AlertsProvider in the tree of the application, any widget under it will
    have access on the JS side to a set of variables and methods to easily access and manipulate
    the current alerts.

    The following variables will be made available in JavaScript:
        alerts: The raw content of the portion of the state where the alerts status is stored
        allAlerts: An array containing all the alerts that exist in the state.
        activeAlerts: An array containing the alerts that have not elapsed yet.
        elapsedAlerts: An array containing the alerts that have elapsed.
        createAlert: Function to create a generic alert. It takes an Alert object.
        createSuccessAlert: Function to create a success alert. It takes an Alert object.
        createWarningAlert: Function to create a warning alert. It takes an Alert object.
        createErrorAlert: Function to create an error alert. It takes an Alert object.
        createInfoAlert: Function to create an info alert. It takes an Alert object.
        dismissAlert: Function to dismiss an alert. It takes an alert id.
        removeAlert: Function to remove an alert. It takes an alert id.
        clearAlerts: Function to remove all the alerts. It takes no arguments.

    Example:
        with AlertsProvider() as alerts_provider:
            html.Button(
                "Create Error",
                click="createErrorAlert({})",
            )

            html.Button(
                "Clear All",
                click="clearAlerts",
            )

            with html.P(v_for="alert in allAlerts", key="alert.id"):
                html.Span("[{{alert.id}}] {{alert.title}} - {{alert.text}}")
                html.Button("Remove", click="removeAlert(alert.id)")
    """

    _next_id = 0

    def __init__(
        self,
        children=None,
        name=DEFAULT_ALERTS_KEY,
        alerts_slot_prop=ALERTS_SLOT_PROP,
        all_alerts_slot_prop=ALL_ALERTS_SLOT_PROP,
        active_alerts_slot_prop=ACTIVE_ALERTS_SLOT_PROP,
        elapsed_alerts_slot_prop=ELAPSED_ALERTS_SLOT_PROP,
        create_alert_slot_prop=CREATE_ALERT_SLOT_PROP,
        create_success_alert_slot_prop=CREATE_SUCCESS_ALERT_SLOT_PROP,
        create_warning_alert_slot_prop=CREATE_WARNING_ALERT_SLOT_PROP,
        create_error_alert_slot_prop=CREATE_ERROR_ALERT_SLOT_PROP,
        create_info_alert_slot_prop=CREATE_INFO_ALERT_SLOT_PROP,
        dismiss_alert_slot_prop=DISMISS_ALERT_SLOT_PROP,
        remove_alert_slot_prop=REMOVE_ALERT_SLOT_PROP,
        clear_alerts_slot_prop=CLEAR_ALERTS_SLOT_PROP,
        **kwargs,
    ):
        """AlertsProvider constructor

        Args:
            children: Children of this widget
                Defaults to None.
            name: The key in the state where the alerts are stored.
                Defaults to "trame__alerts".
            alerts_slot_prop: Name of the injected JS variable containing the raw alerts state.
                Defaults to "alerts".
            all_alerts_slot_prop: Name of the injected JS variable containing an array of all the alerts.
                Defaults to "allAlerts".
            active_alerts_slot_prop: Name of the injected JS variable containing an array of the active alerts.
                Defaults to "activeAlerts".
            elapsed_alerts_slot_prop: Name of the injected JS variable containing an array of the elapsed alerts.
                Defaults to "elapsedAlerts".
            create_alert_slot_prop: Name of the JS injected function that creates a generic alert.
                Defaults to "createAlert".
            create_success_alert_slot_prop: Name of the injected JS function that creates a success alert.
                Defaults to "createSuccessAlert".
            create_warning_alert_slot_prop: Name of the injected JS function that creates a warning alert.
                Defaults to "createWarningAlert".
            create_error_alert_slot_prop: Name of the injected JS function that creates an error alert.
                Defaults to "createErrorAlert".
            create_info_alert_slot_prop: Name of the injected JS function that creates an info alert.
                Defaults to "createInfoAlert".
            dismiss_alert_slot_prop: Name of the injected JS function that dismisses an alert.
                Defaults to "dismissAlert".
            remove_alert_slot_prop: Name of the injected JS function that removes an alert.
                Defaults to "removeAlert".
            clear_alerts_slot_prop: Name of the injected JS function that removes all alert.
                Defaults to "clearAlerts".
        """
        slot_props_names = {
            ALERTS_SLOT_PROP: alerts_slot_prop,
            ALL_ALERTS_SLOT_PROP: all_alerts_slot_prop,
            ACTIVE_ALERTS_SLOT_PROP: active_alerts_slot_prop,
            ELAPSED_ALERTS_SLOT_PROP: elapsed_alerts_slot_prop,
            CREATE_ALERT_SLOT_PROP: create_alert_slot_prop,
            CREATE_SUCCESS_ALERT_SLOT_PROP: create_success_alert_slot_prop,
            CREATE_WARNING_ALERT_SLOT_PROP: create_warning_alert_slot_prop,
            CREATE_ERROR_ALERT_SLOT_PROP: create_error_alert_slot_prop,
            CREATE_INFO_ALERT_SLOT_PROP: create_info_alert_slot_prop,
            DISMISS_ALERT_SLOT_PROP: dismiss_alert_slot_prop,
            REMOVE_ALERT_SLOT_PROP: remove_alert_slot_prop,
            CLEAR_ALERTS_SLOT_PROP: clear_alerts_slot_prop,
        }

        # Place the specific slot_props_names for this instance of the AlertsProvider
        # into a unique location in the state
        slot_props_names_state_key = f"{name}_slot_props_{AlertsProvider._next_id}"
        AlertsProvider._next_id += 1

        # Bind events internally, unless overridden
        kwargs.setdefault("on_create_alert", (self._create_alert, "[$event]"))
        kwargs.setdefault("on_create_success_alert", (self._create_success_alert, "[$event]"))
        kwargs.setdefault("on_create_warning_alert", (self._create_warning_alert, "[$event]"))
        kwargs.setdefault("on_create_error_alert", (self._create_error_alert, "[$event]"))
        kwargs.setdefault("on_create_info_alert", (self._create_info_alert, "[$event]"))
        kwargs.setdefault("on_dismiss_alert", (self._dismiss_alert, "[$event]"))
        kwargs.setdefault("on_remove_alert", (self._remove_alert, "[$event]"))
        kwargs.setdefault("on_clear_alerts", self._clear_alerts)

        super().__init__(
            "trame-alerts-provider",
            alerts=(name,),
            slot_props_names=(slot_props_names_state_key, slot_props_names),
            **kwargs,
        )

        self._attr_names += [
            "alerts",
            ("slot_props_names", "slotPropsNames"),
        ]

        self._event_names += [
            ("on_create_alert", "onCreateAlert"),
            ("on_create_success_alert", "onCreateSuccessAlert"),
            ("on_create_warning_alert", "onCreateWarningAlert"),
            ("on_create_error_alert", "onCreateErrorAlert"),
            ("on_create_info_alert", "onCreateInfoAlert"),
            ("on_dismiss_alert", "onDismissAlert"),
            ("on_remove_alert", "onRemoveAlert"),
            ("on_clear_alerts", "onClearAlerts"),
        ]

        assert self.server

        alerts_service = get_alerts_service(self.server, name)

        assert alerts_service

        self._alerts_service = alerts_service

        self._attributes["slot"] = f'v-slot="{{ { ", ".join(slot_props_names.values()) } }}"'

    @property
    def alerts_service(self):
        """The AlertsService associated with this AlertsProvider"""
        return self._alerts_service

    @property
    def create_alert(self):
        """Creates a new alert

        Args:
            type: Type of alert being created ("success", "warning", "error", "info")
            title: A short description of the alert.
            text: A longer description of the alert.
            timeout: Amount of time in ms after which the alert will be considered elapsed.
            persistent: Whether the alert will be kept in the state after its timeout has elapsed.

        Returns:
            int: The unique id of the alert.
        """
        return self.alerts_service.create_alert

    @property
    def create_success_alert(self):
        """Specialized version of create_alert() for success alerts."""
        return self.alerts_service.create_success_alert

    @property
    def create_warning_alert(self):
        """Specialized version of create_alert() for warning alerts."""
        return self.alerts_service.create_warning_alert

    @property
    def create_error_alert(self):
        """Specialized version of create_alert() for error alerts."""
        return self.alerts_service.create_error_alert

    @property
    def create_info_alert(self):
        """Specialized version of create_alert() for info alerts."""
        return self.alerts_service.create_info_alert

    @property
    def dismiss_alert(self):
        """Dismiss an alert (i.e. mark it elapsed)

        Args:
            id: The id of the alert to be dismissed

        Returns:
            bool: Whether an alert has actually been dismissed
        """
        return self.alerts_service.dismiss_alert

    @property
    def remove_alert(self):
        """Remove an alert from the state

        Args:
            id: The id of the alert to be removed

        Returns:
            bool: Whether an alert has actually been removed
        """
        return self.alerts_service.remove_alert

    @property
    def clear_alerts(self):
        """Remove all the alerts from the state."""
        return self.alerts_service.clear_alerts

    def _create_alert(self, alert):
        self.create_alert(**alert)

    def _create_success_alert(self, alert):
        self.create_success_alert(**alert)

    def _create_warning_alert(self, alert):
        self.create_warning_alert(**alert)

    def _create_error_alert(self, alert):
        self.create_error_alert(**alert)

    def _create_info_alert(self, alert):
        self.create_info_alert(**alert)

    def _dismiss_alert(self, id):
        self.dismiss_alert(id)

    def _remove_alert(self, id):
        self.remove_alert(id)

    def _clear_alerts(self):
        self.clear_alerts()
