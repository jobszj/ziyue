# 优化提示词，等图片服务搭建好之后再优化
# 创建任务将任务存储在Redis中，并调用算法服务，一次提交一个任务

import uuid
from flask_login import current_user
from applications.common.constant import TaskType, TaskStatus, Model
from applications.common.constant import MediaType, TaskType, TaskStatus, Model
from applications.core.midjourney.mj import dmx_mj_generate_image
from applications.init import db
from applications.models import Tasks

def generate_task(args):
    task_id = str(uuid.uuid4())
    user_id = current_user.id
    user_name = current_user.username
    img = args.get("imageUrl")
    prompt = args.get("prompt")
    quantity = args.get("quantity")
    task_type = TaskType.img2img.value if img else TaskType.txt2img.value
    task_model = Model.SD.value if args.get("model") == Model.SD.value else Model.MJ.value
    task = Tasks(task_id=task_id, task_type=task_type, prompt=prompt, quantity=quantity, task_model=task_model, goods_pic=img, user_id=user_id, user_name = user_name, status=TaskStatus.PENDING.value)
    db.session.add(task)
    db.session.commit()
    return task_id


