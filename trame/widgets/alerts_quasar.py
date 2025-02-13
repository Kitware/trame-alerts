from trame_alerts.quasar.widgets import *  # noqa F403


def initialize(server):
    from trame_alerts.quasar import module

    server.enable_module(module)
