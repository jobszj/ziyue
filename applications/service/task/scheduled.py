# 定时任务函数
import asyncio
import datetime

from apscheduler.schedulers.background import BackgroundScheduler
from applications.common.constant import TaskStatus, TaskType, Model
from applications.core.deepclaude.manager import model_manager
from applications.core.sdlt.sdlt import txt_image_sdlt, image_image_sdlt
from applications.init import db
from applications.models import Tasks
from applications.service.expand.expand import expand


# 初始化调度器
def init_scheduler(app):
    scheduler = BackgroundScheduler()

    # 将任务包装为带上下文的函数
    def scheduled_task_with_context():
        with app.app_context():
            # 从数据库MYSQL中查询任务
            tasks = Tasks.query.filter(Tasks.status == TaskStatus.PENDING.value).all()
            print("查询到的任务", tasks)
            for task in tasks:
                # 更新任务状态为running
                task.status = TaskStatus.RUNNING.value
                db.session.commit()
                # 获取图片数量
                total = task.quantity
                if total > 1:
                    for i in range(total):
                        # 对提示词进行加工
                        body = {
                            "messages": [{
                                "role": "user",
                                "content": task.prompt,
                            }],
                            "model": "deepgeminipro"
                        }
                        p = asyncio.run(model_manager.process_request(body))
                        content = p.get("choices")[0].get("message").get("content")
                        print("获取的提示词", p, content)
                        # 调用生成图片服务
                        if task.task_model == Model.SD.value:
                            # 调用sdlt服务
                            pass
                        else:
                            # 调用MJ
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
                    # 调用生成图片服务
                    if task.task_model == Model.SD.value:
                        # 调用sdlt服务
                        if task.task_type == TaskType.txt2img.value:
                            # 调用sdlt的文生图服务
                            txt_image_sdlt(prompt_en, negative_prompt)
                        else:
                            # 调用sdlt的图生图服务
                            image_image_sdlt(prompt_en, negative_prompt, task.goods_pic)
                    elif task.task_model == Model.MJ.value:
                        # 调用MJ
                        # discord_mj_generate_image(prompt_en)
                        pass
                    else:
                        pass

            # 更新任务状态为completed
            task.status = TaskStatus.COMPLETED.value
            task.finish_at = datetime.datetime.now()
            db.session.commit()

    # 添加任务
    scheduler.add_job(scheduled_task_with_context, 'interval', seconds=30)
    scheduler.start()