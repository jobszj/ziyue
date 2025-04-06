# 创建sys
from flask import Blueprint, Flask
from applications.view.magic.script import bp as script_bp
from applications.view.magic.image import bp as image_bp
from applications.view.magic.deepclaude import bp as deepclaude_bp
from applications.view.magic.tag import bp as tag_bp
from applications.view.magic.task import bp as task_bp

magic_bp = Blueprint('magic', __name__, url_prefix='/magic')

def register_magic_bps(app: Flask):
    # 在admin_bp下注册子蓝图
    magic_bp.register_blueprint(script_bp)
    magic_bp.register_blueprint(image_bp)
    magic_bp.register_blueprint(deepclaude_bp)
    magic_bp.register_blueprint(tag_bp)
    magic_bp.register_blueprint(task_bp)
    app.register_blueprint(magic_bp)