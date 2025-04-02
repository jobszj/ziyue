# -*- ecoding: utf-8 -*-
# @Author: anyang
# @Time: 2024/4/5

from support.mj_config import MjConfig
from support.Injector import injector
from wss.mj_wss_manager import MjWssManager

def init_midjourney():
    # 从injector获取mj_config
    mj_config = injector.get(MjConfig)
    
    # 启动 Celery worker
    # subprocess.Popen(['celery', '-A', 'celery_module.celery_app', 'worker', '--loglevel=INFO','-c',"1"])

    # 是否开启新的线程启动对discord_bot的wss监听
    # if mj_config.mj_config["common"]["launch_discord_bot"]:
    mj_wss_manager = injector.get(MjWssManager)
    mj_wss_manager.start_all()


