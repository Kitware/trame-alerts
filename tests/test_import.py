def test_core_import():
    from trame_alerts.core.widgets import AlertsProvider  # noqa: F401
    from trame_alerts.core.service import AlertsService, get_alerts_service  # noqa: F401

    # Widgets are also importable via the trame namespace
    from trame.widgets.alerts import AlertsProvider  # noqa: F401,F811


def test_quasar_import():
    from trame_alerts.quasar.widgets import AlertsPopup, AlertsList, AlertsCount  # noqa: F401

    # Widgets are also importable via the trame namespace
    from trame.widgets.alerts_quasar import AlertsPopup, AlertsList, AlertsCount  # noqa: F401,F811


def test_vuetify_import():
    from trame_alerts.vuetify.widgets import AlertsPopup, AlertsList, AlertsCount  # noqa: F401

    # Widgets are also importable via the trame namespace
    from trame.widgets.alerts_vuetify import AlertsPopup, AlertsList, AlertsCount  # noqa: F401,F811
