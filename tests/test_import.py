def test_core_import():
    from trame_alerts.core.widgets import AlertsProvider  # noqa: F401
    from trame_alerts.core.service import AlertsService, get_alerts_service  # noqa: F401

    # Widgets are also importable via the trame namespace
    from trame.widgets.alerts import AlertsProvider  # noqa: F401,F811
