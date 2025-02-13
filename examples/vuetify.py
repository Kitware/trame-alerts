from trame.app import get_server
from trame.widgets import vuetify3 as vuetify, html, alerts, alerts_vuetify
from trame.ui.vuetify3 import SinglePageWithDrawerLayout


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
            alerts_provider = alerts.AlertsProvider(trame_server=self.server)
            # Optionally bind alerts_provider methods to the controller to make them
            # accessible throughout the application
            self.ctrl.create_warning_alert = alerts_provider.create_warning_alert
            self.ctrl.create_error_alert = alerts_provider.create_error_alert

            with SinglePageWithDrawerLayout(self.server) as layout:
                self._ui = layout

                layout.root = alerts_provider

                layout.title.set_text("Trame Alerts")

                layout.drawer.location = "right"
                layout.drawer.width = 500

                with layout.toolbar:
                    vuetify.VSpacer()
                    alerts_vuetify.AlertsCount()

                with layout.drawer:
                    alerts_vuetify.AlertsList()

                with layout.content:
                    vuetify.VBtn(
                        "Add Warning",
                        click=lambda: alerts_provider.create_warning_alert(
                            text="This is a warning message", persistent=True
                        ),
                    )

                    vuetify.VBtn(
                        "Add Error",
                        click="""createErrorAlert({
                            text: 'This is an error message',
                            persistent: true,
                        })""",
                    )

                    vuetify.VBtn(
                        "Add Success",
                        click="""createSuccessAlert({
                            text: 'This is a success message',
                            persistent: true,
                        })""",
                    )

                    vuetify.VBtn(
                        "Add Info",
                        click="""createInfoAlert({
                            text: 'This is an info message',
                            persistent: true,
                        })""",
                    )

                    vuetify.VBtn(
                        "Clear All",
                        click="clearAlerts",
                    )

                    html.Pre("{{ alerts }}")

                alerts_vuetify.AlertsPopup()

        return self._ui


def main(server=None, *args, **kwargs):
    app = AlertsApp(server)
    app.ui

    app.server.start(**kwargs)


if __name__ == "__main__":
    main()
