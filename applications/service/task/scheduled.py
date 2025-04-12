# 定时任务函数
import asyncio
import datetime
import random
from itertools import product

from apscheduler.schedulers.background import BackgroundScheduler
from applications.common.constant import TaskStatus, TaskType, Model
from applications.common.qiniu import convert_url_to_data_url
from applications.core.deepclaude.manager import model_manager
from applications.core.midjourney.mj import txt_image_mj, image_image_mj
from applications.core.sdlt.sdlt import txt_image_sdlt, image_image_sdlt
from applications.init import db
from applications.models import Tasks, Aigc, Tag
from applications.service.expand.expand import expand, expand_tag, expand_tag_weight

# 初始化调度器
def init_scheduler(app):
    scheduler = BackgroundScheduler()

    # 将任务包装为带上下文的函数
    def scheduled_task_with_context():
        with app.app_context():
            # 从数据库MYSQL中查询任务
            tasks = Tasks.query.filter(Tasks.status == TaskStatus.PENDING.value).all()
            for task in tasks:
                # 更新任务状态为running
                task.status = TaskStatus.RUNNING.value
                db.session.commit()
                # 获取图片数量
                total = task.quantity
                if total > 1:
                    # 获取所有标签，组装成一个数组
                    all_tags = Tag.query.all()
                    second_tags = []
                    third_tag = []
                    for tag in all_tags:
                        if tag.parent_id == 1:
                            second_tags.append(tag)
                    for j in range(len(second_tags)):
                        id = second_tags[j].id
                        tag_name = []
                        for t in all_tags:
                            if id == t.parent_id:
                                tag_name.append(t.tag_name)
                        third_tag.append(tag_name)
                    combinations = list(product(*third_tag))
                    # 从数组中随机选择对应的标签数量生成提示词。
                    selected = random.sample(combinations, total)
                    for sel in selected:
                        # 对提示词进行加工
                        prompt_new, negative_prompt = expand_tag(task.prompt, sel)
                        # 执行任务
                        body = {
                            "messages": [{
                                "role": "user",
                                "content": prompt_new,
                            }],
                            "model": "deepgeminipro"
                        }
                        p = asyncio.run(model_manager.process_request(body))
                        prompt_en = p.get("choices")[0].get("message").get("content")
                        # 生成一个随机数4位
                        index = str(random.randint(10000, 99999))
                        sub_task_id = str(task.task_id)+ "-" + index
                        state = task.task_id + "%" + sub_task_id
                        # 调用生成图片服务
                        if task.task_model == Model.SD.value:
                            # 调用sdlt服务
                            if task.task_type == TaskType.txt2img.value:
                                # 调用sdlt的文生图服务
                                pic_url = txt_image_sdlt(prompt_en, negative_prompt)
                            else:
                                # 调用sdlt的图生图服务
                                pic_url = image_image_sdlt(prompt_en, negative_prompt, task.goods_pic)
                            aigc = Aigc(task_id=task.task_id, sub_task_id=sub_task_id, sub_task_tags=str(sel), prompt_en=prompt_en, prompt_zh=task.prompt,
                                        neg_prompt=negative_prompt, aigc_url=pic_url)
                            db.session.add(aigc)
                            db.session.commit()
                        elif task.task_model == Model.MJ.value:
                            # 调用MJ
                            if task.task_type == TaskType.txt2img.value:
                                # 调用mj的文生图服务
                                # 对提示词增加权重因子
                                txt_image_mj(prompt_en, str(state))
                            else:
                                # 调用mj的图生图服务，# 对提示词增加权重因子
                                pro = expand_tag_weight(prompt_en)
                                # 将图片地址转化为data url
                                data_url = convert_url_to_data_url(task.goods_pic)
                                image_image_mj(pro, data_url, str(state))
                            # mj是四张照片，所以一次需要插入四条数据
                            aigc11 = Aigc(task_id=task.task_id, sub_task_id=sub_task_id+ "-" + "1", sub_task_tags=str(sel),
                                         prompt_en=prompt_en, prompt_zh=prompt_new, neg_prompt=negative_prompt)
                            aigc22 = Aigc(task_id=task.task_id, sub_task_id=sub_task_id + "-" + "2", sub_task_tags=str(sel),
                                         prompt_en=prompt_en, prompt_zh=prompt_new, neg_prompt=negative_prompt)
                            aigc33 = Aigc(task_id=task.task_id, sub_task_id=sub_task_id + "-" + "3", sub_task_tags=str(sel),
                                          prompt_en=prompt_en, prompt_zh=prompt_new, neg_prompt=negative_prompt)
                            aigc44 = Aigc(task_id=task.task_id, sub_task_id=sub_task_id + "-" + "4",
                                          sub_task_tags=str(sel),
                                          prompt_en=prompt_en, prompt_zh=prompt_new, neg_prompt=negative_prompt)
                            db.session.add_all([aigc11, aigc22, aigc33, aigc44])
                            db.session.commit()
                        else:
                            pass


                else:
                    # 对提示词进行加工
                    prompt_new, negative_prompt = expand(task.prompt)
                    # 执行任务
                    body = {
                        "messages": [{
                            "role": "user",
                            "content": prompt_new,
                        }],
                        "model": "deepgeminipro"
                    }
                    p = asyncio.run(model_manager.process_request(body))
                    prompt_en = p.get("choices")[0].get("message").get("content")
                    print("获取的提示词", p, prompt_en)
                    # 生成一个随机数4位
                    index = str(random.randint(10000, 99999))
                    sub_task_id = str(task.task_id) + "-" + index + "-" + "1"
                    state = task.task_id + "%" + sub_task_id
                    # 调用生成图片服务
                    if task.task_model == Model.SD.value:
                        # 调用sdlt服务
                        if task.task_type == TaskType.txt2img.value:
                            # 调用sdlt的文生图服务
                            pic_url = txt_image_sdlt(prompt_en, negative_prompt)
                        else:
                            # 调用sdlt的图生图服务
                            pic_url = image_image_sdlt(prompt_en, negative_prompt, task.goods_pic)
                        # sdlt是同步返回图片地址
                        aigc = Aigc(task_id=task.task_id, sub_task_id=sub_task_id, prompt_en=prompt_en, prompt_zh=task.prompt,
                                    neg_prompt=negative_prompt, aigc_url=pic_url)
                        db.session.add(aigc)
                        db.session.commit()

                    elif task.task_model == Model.MJ.value:
                        # 调用MJ
                        if task.task_type == TaskType.txt2img.value:
                            # 调用mj的文生图服务
                            # 对提示词增加权重因子
                            txt_image_mj(prompt_en, state)
                        else:
                            # 调用mj的图生图服务，# 对提示词增加权重因子
                            pro = expand_tag_weight(prompt_en)
                            pic = convert_url_to_data_url(task.goods_pic)
                            image_image_mj(pro, pic, state)
                    else:
                        pass
                    # mj是四张照片，所以一次需要插入四条数据
                    aigc2 = Aigc(task_id=task.task_id, sub_task_id=sub_task_id,
                                 prompt_en=prompt_en, prompt_zh=prompt_new, neg_prompt=negative_prompt)
                    db.session.add(aigc2)
                    db.session.commit()
                # 更新任务状态为completed
                task.status = TaskStatus.COMPLETED.value
                task.finish_at = datetime.datetime.now()
                db.session.commit()


    # 添加任务
    scheduler.add_job(scheduled_task_with_context, 'interval', seconds=30)
    scheduler.start()

