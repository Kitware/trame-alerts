from trame_client.widgets.core import AbstractElement

from trame_alerts.vuetify import module

__all__ = [
    "AlertsPopup",
    "AlertsList",
    "AlertsCount",
]


class HtmlElement(AbstractElement):
    def __init__(self, _elem_name, children=None, **kwargs):
        super().__init__(_elem_name, children, **kwargs)
        if self.server:
            self.server.enable_module(module)


class AlertsPopup(HtmlElement):
    """Vuetify widget to display popups for a set of alerts"""

    def __init__(self, **kwargs):
        kwargs.setdefault("alerts", ("activeAlerts",))
        kwargs.setdefault("remove", "removeAlert")

        super().__init__(
            "trame-alerts-vuetify-popup",
            **kwargs,
        )
        self._attr_names += [
            "alerts",
        ]
        self._event_names += [
            "remove",
        ]


class AlertsList(HtmlElement):
    """Vuetify widget to list a set of alerts"""

    def __init__(self, **kwargs):
        kwargs.setdefault("alerts", ("elapsedAlerts",))
        kwargs.setdefault("remove", "removeAlert")

        super().__init__(
            "trame-alerts-vuetify-list",
            **kwargs,
        )
        self._attr_names += [
            "alerts",
        ]
        self._event_names += [
            "remove",
        ]


class AlertsCount(HtmlElement):
    """Vuetify widget to show an alert counter"""

    def __init__(self, **kwargs):
        kwargs.setdefault("alerts", ("elapsedAlerts",))

        super().__init__(
            "trame-alerts-vuetify-count",
            **kwargs,
        )
        self._attr_names += [
            "alerts",
        ]
        self._event_names += [
            "click",
        ]
