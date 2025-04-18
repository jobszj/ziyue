from applications.view.magic import register_magic_bps
from applications.view.system import register_system_bps
from applications.view.plugin import register_plugin_views


def init_bps(app):
    register_system_bps(app)
    register_magic_bps(app)
    register_plugin_views(app)

