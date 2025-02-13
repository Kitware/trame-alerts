from typing import TypedDict, Literal, Union

import asyncio

from trame_server.core import Server
from trame_server.utils import asynchronous

DEFAULT_ALERTS_KEY = "trame__alerts"

AlertType = Literal["info", "success", "warning", "error"]


class Alert(TypedDict):
    """Dictionary describing an alert

    Attributes:
        id: Unique id of the alert.
        type: Type of the alert ("success", "warning", "error", "info").
        title: A short description of the alert.
        text: A longer description of the alert.
        timeout: Amount of time in ms after which the alert will be considered elapsed.
        elapsed: Whether the alert has reached its timeout.
        persistent: Whether the alert will be kept in the state after its timeout has elapsed.
    """

    id: int
    type: AlertType
    title: str
    text: str
    timeout: int
    elapsed: bool
    persistent: bool


class AlertsService:
    """Keep track of notifications/alerts in the State

    This utility class provides methods to create and remove various types of
    alerts and keeps track of their status in a managed section of the Trame State.

    Example:

        alerts_service = AlertsService()
        alert_id = alerts_service.create_warning_alert(
            title="Warning!",
            text="A longer description of what the warning is about",
            timeout=5000,
        )
        alerts_service.remove_alert(alert_id)
    """

    _next_id = 0

    def __init__(self, server: Server, alerts_key=DEFAULT_ALERTS_KEY):
        """AlertsService constructor

        Args:
            server: The server this instance will be bound to.
            alerts_key: The key in the state where the alerts will be stored.
                Defaults to "trame__alerts".
        """
        self._server = server
        self._alerts_key = alerts_key
        self.state.setdefault(self._alerts_key, {})

    @property
    def state(self):
        """The trame state associated to this AlertsService"""
        return self._server.state

    def create_alert(
        self,
        type: AlertType,
        title: str,
        text: str = "",
        timeout: int = 5000,
        persistent: bool = False,
    ) -> int:
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
        alert_id = AlertsService._next_id
        AlertsService._next_id += 1

        alert: Alert = {
            "id": alert_id,
            "type": type,
            "title": title,
            "text": text,
            "timeout": timeout,
            "elapsed": False,
            "persistent": persistent,
        }

        alerts = self.state_alerts.copy()
        alerts[alert_id] = alert

        with self.state:
            self.state_alerts = alerts

        if timeout > 0:
            if persistent:
                on_timeout_fn = self.dismiss_alert
            else:
                on_timeout_fn = self.remove_alert

            asynchronous.create_task(AlertsService._defer(timeout, on_timeout_fn, alert_id))

        return alert_id

    @staticmethod
    async def _defer(delay_ms, fn, *args, **kwargs):
        """Asynchronously defer the invocation of a function."""
        await asyncio.sleep(delay_ms / 1000)
        fn(*args, **kwargs)

    @property
    def state_alerts(self):
        """The alerts currently in the state."""
        return self.state.__getattr__(self._alerts_key)

    @state_alerts.setter
    def state_alerts(self, alerts):
        """Update the alerts in the state."""
        return self.state.__setattr__(self._alerts_key, alerts)

    def create_info_alert(
        self,
        title: str = "Info",
        text: str = "",
        timeout: int = 5000,
        persistent: bool = False,
    ) -> int:
        """Specialized version of create_alert() for info alerts."""
        return self.create_alert("info", title, text, timeout, persistent)

    def create_success_alert(
        self,
        title: str = "Success",
        text: str = "",
        timeout: int = 5000,
        persistent: bool = False,
    ) -> int:
        """Specialized version of create_alert() for success alerts."""
        return self.create_alert("success", title, text, timeout, persistent)

    def create_warning_alert(
        self,
        title: str = "Warning",
        text: str = "",
        timeout: int = 5000,
        persistent: bool = False,
    ) -> int:
        """Specialized version of create_alert() for warning alerts."""
        return self.create_alert("warning", title, text, timeout, persistent)

    def create_error_alert(
        self,
        title: str = "Error",
        text: str = "",
        timeout: int = 5000,
        persistent: bool = False,
    ) -> int:
        """Specialized version of create_alert() for error alerts."""
        return self.create_alert("error", title, text, timeout, persistent)

    def dismiss_alert(self, id: int) -> bool:
        """Dismiss an alert (i.e. mark it elapsed)

        Args:
            id: The id of the alert to be dismissed

        Returns:
            bool: Whether an alert has actually been dismissed
        """
        if self.state_alerts.get(id) is None:
            return False

        if self.state_alerts[id]["elapsed"]:
            return False

        alerts = self.state_alerts.copy()
        alert = alerts[id].copy()
        alert["elapsed"] = True
        alerts[id] = alert

        with self.state:
            self.state_alerts = alerts

        return True

    def remove_alert(self, id) -> bool:
        """Remove an alert from the state

        Args:
            id: The id of the alert to be removed

        Returns:
            bool: Whether an alert has actually been removed
        """
        if self.state_alerts.get(id) is None:
            return False

        alerts = self.state_alerts.copy()
        del alerts[id]

        with self.state:
            self.state_alerts = alerts

        return True

    def clear_alerts(self):
        """Remove all the alerts from the state."""
        with self.state:
            self.state_alerts = {}


def get_alerts_service(
    server: Server,
    alerts_key: str = DEFAULT_ALERTS_KEY,
    create_if_missing: bool = True,
) -> Union[AlertsService, None]:
    """Get the AlertsService associated with the given server and alerts_key

    Args:
        server: The server bound to the alerts service.
        alerts_key: The key in the state where the alerts are stored.
            Defaults to "trame__alerts".
        create_if_missing: If a service for the given server and alerts_key
            doesn't exist, create one. Defaults to True.

    Returns:
        Union[AlertsService, None]: The alerts service if found or None
    """
    available_services = server.context.setdefault("__alert_services", {})

    alert_service = available_services.get(alerts_key)

    if alert_service is None and create_if_missing:
        alert_service = AlertsService(server, alerts_key)
        available_services[alerts_key] = alert_service

    return alert_service
