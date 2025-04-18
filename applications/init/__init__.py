from flask import Flask

from .init_sqlalchemy import db, ma, init_databases
from .init_login import init_login_manager
from .init_template_directives import init_template_directives
from .init_error_views import init_error_views
from .init_upload import init_upload
from .init_migrate import init_migrate
from .init_session import init_session


def init_plugs(app: Flask) -> None:
    init_login_manager(app)
    init_databases(app)
    init_template_directives(app)
    init_error_views(app)
    init_upload(app)
    init_migrate(app)
    init_session(app)