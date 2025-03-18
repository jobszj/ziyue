from flask import Blueprint, render_template
from flask_login import login_required

from applications.common.utils.rights import authorize

bp = Blueprint('script', __name__, url_prefix='/script')
# 脚本生成
@bp.get('/')
@authorize("magic:script:main")
def main():
    return render_template('magic/script.html')