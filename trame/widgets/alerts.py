from trame_alerts.core.widgets import *  # noqa F403


def initialize(server):
    from trame_alerts.core import module

    server.enable_module(module)
