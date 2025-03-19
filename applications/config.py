import logging
from datetime import timedelta

from urllib.parse import quote_plus as urlquote


class BaseConfig:
    SUPERADMIN = 'admin'

    SYSTEM_NAME = 'Admin'
    # 主题面板的链接列表配置
    SYSTEM_PANEL_LINKS = [
    ]

    UPLOADED_PHOTOS_DEST = 'static/upload'
    UPLOADED_FILES_ALLOW = ['gif', 'jpg']
    UPLOADS_AUTOSERVE = True

    # JSON配置
    JSON_AS_ASCII = False

    SECRET_KEY = "magic_20250316"

    # mysql 配置
    MYSQL_USERNAME = "root"
    MYSQL_PASSWORD = "123456"
    MYSQL_HOST = "127.0.0.1"
    MYSQL_PORT = 3306
    MYSQL_DATABASE = "magic"

    # 数据库的配置信息
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{MYSQL_USERNAME}:{urlquote(MYSQL_PASSWORD)}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}?charset=utf8mb4"

    # Redis配置
    REDIS_URL = 'redis://:123456@localhost:6379/8'
    # 默认日志等级
    LOG_LEVEL = logging.WARN
    """
    flask-mail配置
    """
    MAIL_SERVER = 'smtp.qq.com'
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_PORT = 465
    MAIL_USERNAME = '838824656@qq.com'
    MAIL_PASSWORD = 'XXXXX'  # 生成的授权码
    MAIL_DEFAULT_SENDER = MAIL_USERNAME

    # 插件配置，填写插件的文件名名称，默认不启用插件。
    PLUGIN_ENABLE_FOLDERS = []

    """
    session
    """

    PERMANENT_SESSION_LIFETIME = timedelta(days=7)

    SESSION_TYPE = "filesystem" # 默认使用文件系统来保存会话
    SESSION_PERMANENT = False  # 会话是否持久化
    SESSION_USE_SIGNER = True  # 是否对发送到浏览器上 session 的 cookie 值进行加密

