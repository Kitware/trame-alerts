from trame_alerts.vuetify.widgets import *  # noqa F403


def initialize(server):
    from trame_alerts.vuetify import module

    server.enable_module(module)
