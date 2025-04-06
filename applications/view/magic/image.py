from flask import Blueprint, render_template, request
from applications.common.utils.http import table_api
from applications.common.utils.rights import authorize
from applications.service.task.task import generate_task

bp = Blueprint('image', __name__, url_prefix='/image')

# 脚本生成
@bp.get('/')
@authorize("magic:image:main")
def main():
    return render_template("magic/image.html")

# 生成图片表单提交功能接口
@bp.route('/generate', methods=['POST'])
@authorize("magic:image:add", log=True)
def image_generate():
    req_json = request.get_json(force=True)
    # 创建任务并将任务放到MYSQL中
    generate_task(req_json)
    return table_api(msg="生成图片中")


@bp.route('/callback', methods=['POST'])
def upscale_callback():
    req_json = request.get_json(force=True)
    # 创建任务，并直接返回，服务端通过多线程方式实现多任务
    properties = req_json.get("properties").get("progress")
    if properties.get("progress") == "100%":
        pic = properties.get("imageUrl")
        # 将图片保存至七牛云，并记录到数据库中心
        print("生成图片成功")
    print("回调的参数", req_json)
    return table_api(msg="生成图片成功")

