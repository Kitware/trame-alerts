from trame.app import get_server
from trame.widgets import html, quasar, alerts, alerts_quasar
from trame.ui.quasar import QLayout


class AlertsApp:
    def __init__(self, server=None):
        self._server = get_server(server, client_type="vue3")

        self._ui = None

    @property
    def server(self):
        return self._server

    @property
    def state(self):
        return self.server.state

    @property
    def ctrl(self):
        return self.server.controller

    @property
    def ui(self):
        if self._ui is None:
            with QLayout(self.server) as layout:
                self._ui = layout

                with alerts.AlertsProvider() as alerts_provider:
                    # Optionally bind alerts_provider methods to the controller to make them
                    # accessible throughout the application
                    self.ctrl.create_warning_alert = alerts_provider.create_warning_alert
                    self.ctrl.create_error_alert = alerts_provider.create_error_alert
                    # ...

                    with quasar.QHeader():
                        with quasar.QToolbar(classes="shadow-4"):
                            quasar.QToolbarTitle("Trame Alerts")
                            alerts_quasar.AlertsCount(click="drawerRight = !drawerRight")

                    with quasar.QDrawer(
                        v_model=("drawerRight", True),
                        side="right",
                        bordered=True,
                        overlay=True,
                        width=400,
                    ):
                        alerts_quasar.AlertsList()

                    with quasar.QPageContainer():
                        with quasar.QPage(classes="pa-2"):
                            quasar.QBtn(
                                "Add Warning",
                                click=lambda: alerts_provider.create_warning_alert(
                                    text="This is a warning message", persistent=True
                                ),
                            )

                            quasar.QBtn(
                                "Add Error",
                                click="""createErrorAlert({
                                    text: 'This is an error message',
                                    persistent: true,
                                })""",
                            )

                            quasar.QBtn(
                                "Add Success",
                                click="""createSuccessAlert({
                                    text: 'This is a success message',
                                    persistent: true,
                                })""",
                            )

                            quasar.QBtn(
                                "Add Info",
                                click="""createInfoAlert({
                                    text: 'This is an info message',
                                    persistent: true,
                                })""",
                            )

                            quasar.QBtn(
                                "Clear All",
                                click="clearAlerts",
                            )

                            html.Pre("{{ alerts }}")

                    alerts_quasar.AlertsPopup()

        return self._ui


def main(server=None, *args, **kwargs):
    app = AlertsApp(server)
    app.ui

    app.server.start(**kwargs)


if __name__ == "__main__":
    main()
