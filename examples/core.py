from trame.app import get_server
from trame.widgets import html, alerts
from trame.ui.html import DivLayout


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
            with DivLayout(self.server) as layout:
                self._ui = layout

                with alerts.AlertsProvider() as alerts_provider:
                    # Optionally bind alerts_provider methods to the controller to make them
                    # accessible throughout the application
                    self.ctrl.create_warning_alert = alerts_provider.create_warning_alert
                    self.ctrl.create_error_alert = alerts_provider.create_error_alert
                    # ...

                    html.Button(
                        "Add Warning",
                        click=lambda: alerts_provider.create_warning_alert(
                            text="This is a warning message", persistent=True
                        ),
                    )

                    html.Button(
                        "Add Error",
                        click="""createErrorAlert({
                            text: 'This is an error message',
                            persistent: true,
                        })""",
                    )

                    html.Button(
                        "Add Success",
                        click="""createSuccessAlert({
                            text: 'This is a success message',
                            persistent: true,
                        })""",
                    )

                    html.Button(
                        "Add Info",
                        click="""createInfoAlert({
                            text: 'This is an info message',
                            persistent: true,
                        })""",
                    )

                    html.Button(
                        "Clear All",
                        click="clearAlerts",
                    )

                    html.Pre("Active alerts: {{ activeAlerts.length }}")

                    with html.P(v_for="alert in activeAlerts", key="alert.id"):
                        html.Span("[{{alert.id}}] {{alert.title}} - {{alert.text}}")
                        html.Button("Remove", click="removeAlert(alert.id)")

                    html.Pre("Elapsed alerts: {{ elapsedAlerts.length }}")

                    with html.P(v_for="alert in elapsedAlerts", key="alert.id"):
                        html.Span("[{{alert.id}}] {{alert.title}} - {{alert.text}}")
                        html.Button("Remove", click="removeAlert(alert.id)")

                    html.Pre("{{ alerts }}")

        return self._ui


def main(server=None, *args, **kwargs):
    app = AlertsApp(server)
    app.ui

    app.server.start(**kwargs)


if __name__ == "__main__":
    main()
