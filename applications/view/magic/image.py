from flask import Blueprint, render_template, request
from applications.common.utils.http import success_api
from applications.common.utils.rights import authorize
from flask_login import current_user
from applications.common.utils.validate import str_escape

bp = Blueprint('image', __name__, url_prefix='/image')
# 脚本生成
@bp.get('/')
@authorize("magic:image:main")
def main():
    return render_template('magic/image.html')

# 生成图片表单提交功能接口
@bp.route('/generate', methods=['POST'])
# @authorize("magic:image:add", log=True)
def generate_images():
    user = current_user
    req_json = request.get_json(force=True)
    prompt = str_escape(req_json.get('prompt'))
    quantity = str_escape(req_json.get('quantity'))
    model = str_escape(req_json.get('model'))
    imageUrl = str_escape(req_json.get('imageUrl'))
    v = req_json.get('v')
    u = req_json.get('u')
    print(prompt, quantity, model, imageUrl, v, u, user)
    # 优化提示词
    # 创建任务将任务存储在Redis中，并调用算法服务
    # 返回任务ID

    # 向前端返回结果

    return success_api(msg="提交任务成功，图片生成中")