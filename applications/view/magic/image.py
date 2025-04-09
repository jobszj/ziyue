import base64

import requests
from flask import Blueprint, render_template, request

from applications.common.qiniu import upload_image_to_qiniu
from applications.common.utils.http import table_api
from applications.common.utils.rights import authorize
from applications.core.midjourney.mj import mj_image_upscale
from applications.init import db
from applications.service.task.imagetask import generate_task

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

@bp.route('/notify', methods=['POST'])
def notify():
    req_json = request.get_json(force=True)
    print("收到的回调", req_json)
    # 创建任务，并直接返回，服务端通过多线程方式实现多任务
    taskId = req_json.get("id")
    progress = req_json.get("properties").get("progress")
    state = req_json.get("properties").get("state")
    action = req_json.get("properties").get("action")
    print("staeeeete", progress, state, action)
    if (progress == "100%" and action == "IMAGINE"):
        print("staeeeete", state)
        # 调用发达接口将四张图片放大1~4
        for i in range(1, 5):
            mj_image_upscale(taskId, i)
    elif (progress == "100%" and action == "UPSCALE"):
        db.session.execute(
            "UPDATE image_task SET pic_url = %s WHERE sub_task_id = %s",
            (req_json.get("imageUrl"), state)
        )
        db.session.commit()
    return table_api(msg="生成图片中")
