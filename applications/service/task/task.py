# 优化提示词，等图片服务搭建好之后再优化
# 创建任务将任务存储在Redis中，并调用算法服务，一次提交一个任务

import uuid
from flask_login import current_user
from applications.common.constant import MediaType, TaskType, TaskStatus, Model
from applications.core.midjourney.mj import dmx_mj_generate_image
from applications.core.sdlt.sdlt import image_sdlt
from applications.init import db
from applications.models import Tasks, Photo

def generate_task(args):
    task_id = str(uuid.uuid4())
    user_id = current_user.id
    user_name = current_user.username
    img = args.get("imageUrl")
    prompt = args.get("expand")
    quantity = args.get("quantity")
    task_type = TaskType.img2img.value if img else TaskType.txt2img.value
    task_model = Model.SD.value if args.get("model") == Model.SD.value else Model.MJ.value
    task = Tasks(task_id=task_id, task_type=task_type, prompt=prompt, quantity=quantity, task_model=task_model, goods_pic=img, user_id=user_id, user_name = user_name, status=TaskStatus.PENDING.value)
    db.session.add(task)
    db.session.commit()
    return task_id

def generate_image(args):
    # 获取登录用户
    user = current_user
    type = args.get("model")
    # 每次提交创建一个任务ID，任务ID是随机全局唯一，该任务下面拆解成子任务
    # 一张图片一个子任务，每个子任务放入数组中，并生成子任务ID，线程执行时携带子任务ID，
    # 每个子任务提交一次生成图片，生成完成后将任务状态该已完成并从任务队列中删除
    num = args.get("quantity")
    prompt = args.get("prompts")
    if type == 'SD':
        if num > 1:
            for i in range(num):
                sub_task = {
                    "expand": prompt,
                    "negative_prompt": args.get("negative_prompt"),
                    "imageUrl": args.get("imageUrl")
                }
                pic_url = image_sdlt(sub_task)
                # 将图片地址保存至MySQL中
                photo = Photo(name=user.name, mime=user.id, size=MediaType.i, href=pic_url)
                db.session.add(photo)
                db.session.commit()
        # 调用算法服务
        else:
            pic_url = image_sdlt(args)
            # 将图片地址保存至MySQL中
            photo = Photo(name=user.name, mime=user.id, size=MediaType.i, href=pic_url)
            db.session.add(photo)
            db.session.commit()
    else:
        dmx_mj_generate_image(args)
    return None

