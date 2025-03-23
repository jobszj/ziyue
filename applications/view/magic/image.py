from flask import Blueprint, render_template, request
from applications.common.utils.http import success_api, fail_api, table_api
from applications.common.utils.rights import authorize
from flask_login import current_user
from applications.common.utils.validate import str_escape
from applications.core.sdlt.sdlt import image_sdlt
from applications.core.task.task import add_task_to_queue

bp = Blueprint('image', __name__, url_prefix='/image')
# 脚本生成
@bp.get('/')
@authorize("magic:image:main")
def main():
    return render_template('magic/image.html')

# 生成图片表单提交功能接口
@bp.route('/generate', methods=['POST'])
@authorize("magic:image:add", log=True)
def generate_images():
    req_json = request.get_json(force=True)
    print(req_json)
    # 优化提示词，等图片服务搭建好之后再优化
    # 创建任务将任务存储在Redis中，并调用算法服务，一次提交一个任务
    # if(add_task_to_queue(req_json)):
        # 调用算法服务生成图片
    result = image_sdlt(req_json)
    print("生成的图片地址", result)
    return table_api(msg="生成图片成功", data={"src": result})

