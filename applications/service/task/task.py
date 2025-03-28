# 优化提示词，等图片服务搭建好之后再优化
# 创建任务将任务存储在Redis中，并调用算法服务，一次提交一个任务
import uuid
from flask_login import current_user
from applications.common.constant import MediaType
from applications.core.midjourney.mj import mj_generate_image
from applications.core.sdlt.sdlt import image_sdlt
from applications.init import db
from applications.models import Photo


def generate_tasks(args):
    # 获取登录用户
    user = current_user
    type = args.get("model")
    # 每次提交创建一个任务ID，任务ID是随机全局唯一，该任务下面拆解成子任务
    # 一张图片一个子任务，每个子任务放入数组中，并生成子任务ID，线程执行时携带子任务ID，
    # 每个子任务提交一次生成图片，生成完成后将任务状态该已完成并从任务队列中删除
    task_id = uuid.uuid4().hex
    num = args.get("quantity")
    # 对每个人物的prompt调用prompt服务进行优化,是一个数组
    prompts = args.get("prompts")
    if type == 'SD':
        if num > 1:
            for i in range(num):
                sub_task_id = uuid.uuid4().hex
                args["task_id"] = task_id
                args["sub_task_id"] = sub_task_id
                sub_task = {
                    "task_id": task_id,
                    "sub_task_id": sub_task_id,
                    "prompt": prompts,
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
        mj_generate_image(args)
        return None
    return None

