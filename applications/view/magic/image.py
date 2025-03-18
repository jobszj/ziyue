from flask import Blueprint, render_template
from applications.common.utils.rights import authorize

bp = Blueprint('image', __name__, url_prefix='/image')
# 脚本生成
@bp.get('/')
@authorize("magic:image:main")
def main():
    return render_template('magic/image.html')