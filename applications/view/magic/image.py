import time
from flask import Blueprint, render_template, request
from sqlalchemy import text

from applications.common.qiniu import upload_image_to_qiniu_by_url
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
    progress = req_json.get("progress")
    action = req_json.get("action")
    state = req_json.get("state")
    if (progress == "100%" and action == "IMAGINE"):
        print("生成的图片",req_json.get("imageUrl"))
        # 调用发达接口将四张图片放大1~4
        for i in range(1, 5):
            mj_image_upscale(taskId, i, state)
            time.sleep(1)
    elif (progress == "100%" and action == "UPSCALE"):
        sub_task_id = state.split("%")[1]
        index =
        sub_id = sub_task_id + "-" + str(index)
        img = req_json.get("imageUrl")
        # 将图片上传至七牛云
        res_img = upload_image_to_qiniu_by_url(img, 'mj')
        tu = {"res_img": res_img, "sub_task_id": sub_id}
        print("放大的图片", img, res_img, tu)

        db.session.execute(
            text("UPDATE magic_aigc SET aigc_url = :res_img WHERE sub_task_id = :sub_task_id"),
            tu
        )
        db.session.commit()
    return table_api(msg="生成图片中")
