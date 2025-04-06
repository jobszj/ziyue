import datetime

from applications.core.midjourney.entity.mj_scheme import ImagineRequest, QueryImagineStatusRequest, UpscaleRequest, \
    QueryUpscaleStatusRequest, DescribeRequest, BlendRequest, ShortenRequest
from applications.core.midjourney.service.mj_data_service import MjDataService, MjTask
from applications.core.midjourney.support.Injector import injector
from applications.core.midjourney.support.load_balancer import LoadBalancer
from applications.core.midjourney.support.task_controller import TaskController

task_controller = injector.get(TaskController)
mj_data_service = injector.get(MjDataService)
load_balancer = injector.get(LoadBalancer)



async def submit_imagine(imagine_request: ImagineRequest):
    prompt = imagine_request.prompt
    if not prompt:
        return {
            "status": 400,
            "msg": "prompt不能为空",
            "data": None,
        }

    imgs = []
    if imagine_request.imgs:
        for img in imagine_request.imgs:
            image_url = load_balancer.get_discord_http_service().upload_img_if_bs64(img)
            imgs.append(image_url)
    # 将reference_imgs用空格进行拼接
    if len(imgs) > 0:
        image_prompt = " ".join(imgs)
    else:
        image_prompt = ""

    text_prompt = prompt

    if imagine_request.mode == "FAST":
        text_prompt += " --fast"
    elif imagine_request.mode == "RELAX":
        text_prompt += " --relax"

    task = MjTask()
    task.prompt = text_prompt
    task.image_prompt = image_prompt
    task.task_type = "imagine"
    task.task_status = "pending"
    nonce = mj_data_service.next_nonce()
    task.nonce = str(nonce)
    task.create_time = datetime.datetime.now()

    task_id = task_controller.submit_imagine(task)

    return {
        "status": 200,
        "msg": "success",
        "data": {
            "task_id": task_id,
            "task_status": task.task_status,
        },
    }


async def query_imagine_status(body: QueryImagineStatusRequest):
    task_id = body.task_id
    task: MjTask = mj_data_service.get_task_by_task_id(task_id)
    if not task:
        return {
            "status": 10002,
            "msg": f"未查询到任务:task_id:{task_id}",
        }
    else:
        # 根据任务状态返回结果
        image_url = task.image_url
        if image_url:
            image_url = image_url.replace(
                "https://cdn.discordapp.com", "http://discordcdn.aidomore.com")

        return {
            "status": 200,
            "msg": "success",
            "data": {
                "task_id": task.task_id,
                "task_status": task.task_status,
                "image_url": image_url,
                "progress": task.progress,
            },
        }


async def submit_upscale(body: UpscaleRequest):
    task_id = body.task_id
    mode = body.mode
    # index = body.index
    # action_type = body.action_type
    custom_id = body.custom_id

    task: MjTask = mj_data_service.get_task_by_task_id(task_id)
    action_task = MjTask()
    action_task.task_type = "action"
    action_task.create_time = datetime.datetime.now()
    action_task.task_status = "pending"
    action_task.custom_id = custom_id
    action_task.reference_message_id = task.message_id
    nonce = mj_data_service.next_nonce()
    action_task.nonce = str(nonce)
    task_id = task_controller.submit_upscale(action_task)
    return {
        "status": 200,
        "msg": "success",
        "data": {
            "task_id": task_id,
            "task_status": action_task.task_status,
        }
    }


# 查询upscale
async def query_upscale_status(body: QueryUpscaleStatusRequest):
    task_id = body.task_id
    task: MjTask = mj_data_service.get_task_by_task_id(task_id)
    if not task:
        return {
            "status": 10002,
            "msg": f"未查询到任务:task_id:{task_id}"
        }
    else:
        # 根据任务状态返回结果
        image_url = task.image_url
        if image_url:
            image_url = image_url.replace(
                "https://cdn.discordapp.com", "http://discordcdn.aidomore.com")

        return {
            "status": 200,
            "msg": "success",
            "data": {
                "task_id": task.task_id,
                "task_type": task.task_type,
                "task_status": task.task_status,
                "image_url": image_url,
                "progress": task.progress,
                "description": task.description,
                "buttons": task.buttons,
            },
        }


async def submit_describe_func(body: DescribeRequest):
    if not body.img:
        return {
            "status": 10001,
            "msg": "需要传入参考图片"
        }

    task = MjTask()

    task.task_type = "describe"
    task.task_status = "pending"
    nonce = mj_data_service.next_nonce()
    task.nonce = str(nonce)
    task.image_prompt = body.img
    task.create_time = datetime.datetime.now()
    task_id = task_controller.submit_describe(task)
    return {
        "status": 200,
        "msg": "success",
        "data": {
            "task_id": task_id,
            "task_status": task.task_status,
        }
    }


# blend
async def submit_blend_func(body: BlendRequest):
    if not body.imgs:
        return {
            "status": 10001,
            "msg": "需要传入参考图片"
        }
    dimensions = body.dimensions
    task = MjTask()
    task.task_type = "blend"
    task.blend_imgs = body.imgs
    task.task_status = "pending"
    nonce = mj_data_service.next_nonce()
    task.nonce = str(nonce)
    task.dimensions = dimensions
    task.create_time = datetime.datetime.now()
    task_id = task_controller.submit_blend(task)
    return {
        "status": 200,
        "msg": "success",
        "data": {
            "task_id": task_id,
            "task_status": task.task_status,
        }
    }


# shorten
async def shorten(body: ShortenRequest):
    if not body.prompt:
        return {
            "status": 10002,
            "msg": "需要传入prompt"
        }
    
    task = MjTask()
    task.task_type = "shorten"
    task.prompt = body.prompt
    task.task_status = "pending"
    nonce = mj_data_service.next_nonce()
    task.nonce = str(nonce)
    task.create_time = datetime.datetime.now()
    task_id = task_controller.submit_shorten(task)

    return {
        "status": 200,
        "msg": "success",
        "data": {
            "task_id": task_id,
            "task_status": task.task_status,
        }
    }