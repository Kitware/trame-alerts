# trame-alerts

A trame package to manage and display alerts/notification while being agnostic of the widget framework you want to use.
This can be use to report errors and let the user know about the completions of tasks. 

![demo](https://github.com/Kitware/trame-alerts/blob/main/demo.png)

## Installing
Install `trame_alerts` using `pip`
```bash
pip install trame_alerts
```

If you are planning on using the provided vuetify UI widgets to display the alerts run the following:
```bash
pip install trame_alerts[vuetify]
```

If you are planning on using the provided quasar UI widgets to display the alerts run the following:
```bash
pip install trame_alerts[quasar]
```

## Usage
The core component to this library is the `AlertsProvider` widget. This widget manages a portion of the trame state where the status of the alerts is stored, and provides easy access to set of JavaScript variables and functions to any widgets that are its descendants.

```python
from trame.app import get_server
from trame.widgets import html, alerts
from trame.ui.html import DivLayout

server = get_server(client_type="vue3")

with DivLayout(server) as layout:
    with alerts.AlertsProvider():
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

server.start()
```

The following variables are be made available in JavaScript:
- `alerts`: The raw content of the portion of the state where the alerts status is stored
- `allAlerts`: An array containing all the alerts that exist in the state.
- `activeAlerts`: An array containing the alerts that have not elapsed yet.
- `elapsedAlerts`: An array containing the alerts that have elapsed.
- `createAlert`: Function to create a generic alert. It takes an Alert object.
- `createSuccessAlert`: Function to create a success alert. It takes an Alert object.
- `createWarningAlert`: Function to create a warning alert. It takes an Alert object.
- `createErrorAlert`: Function to create an error alert. It takes an Alert object.
- `createInfoAlert`: Function to create an info alert. It takes an Alert object.
- `dismissAlert`: Function to dismiss an alert. It takes an alert id.
- `removeAlert`: Function to remove an alert. It takes an alert id.
- `clearAlerts`: Function to remove all the alerts. It takes no arguments.


## Examples

Refer to the [`examples`](examples/) folder for minimal complete applications that use the core library as well as the vuetify and quasar UI implementation.


## Developing

Build and install the core Vue components

```bash
    cd vue-components/core
    npm i
    npm run build
    cd -
```

Build and install the vuetify Vue components

```bash
    cd vue-components/vuetify
    npm i
    npm run build
    cd -
```

Build and install the quasar Vue components

```bash
    cd vue-components/quasar
    npm i
    npm run build
    cd -
```

Install the library

```bash
pip install -e ".[dev,vuetify,quasar]"
```

## License

`trame-alerts` is made available under the Apache License, Version 2.0. For more details, see [LICENSE](LICENSE)


## Community

[Trame](https://kitware.github.io/trame) | [Discussions](https://github.com/Kitware/trame/discussions) | [Issues](https://github.com/Kitware/trame/issues) | [Contact Us](https://www.kitware.com/contact-us/)


## Enjoying trame?

Share your experience [with a testimonial](https://github.com/Kitware/trame/issues/18) or [with a brand approval](https://github.com/Kitware/trame/issues/19).


## JavaScript dependency

This package optionally depends on [`trame-vuetify`](https://github.com/Kitware/trame-vuetify) and [`trame-quasar`](https://github.com/Kitware/trame-quasar), but does not bundle any specific external JavaScript library.
