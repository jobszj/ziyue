import os
from flask import Flask

from applications.core.midjourney.init_mj import init_midjourney
from applications.init.script import init_script
from applications.config import BaseConfig
from applications.init import init_plugs
from applications.service.task.scheduled import init_scheduler
from applications.view import init_bps

def create_app():
    app = Flask(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
    # 引入配置
    app.config.from_object(BaseConfig)

    # 注册flask组件
    init_plugs(app)

    # 注册蓝图,注册api蓝图
    init_bps(app)

    # 注册命令
    init_script(app)

    # 注册定时任务
    init_scheduler(app)

    # 注册midjourney
    init_midjourney()

    return app
