import os
from flask import Flask
from applications.common.script import init_script
from applications.config import BaseConfig
from applications.init import init_plugs
from applications.api import init_api_bps
from applications.view import init_bps


def create_app():
    app = Flask(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
    # 引入配置
    app.config.from_object(BaseConfig)

    # 注册flask组件
    init_plugs(app)

    # 注册蓝图,注册api蓝图
    init_bps(app)
    init_api_bps(app)

    # 注册命令
    init_script(app)

    return app
