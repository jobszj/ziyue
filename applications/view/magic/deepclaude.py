from flask import Blueprint, request
from applications.core.deepclaude.manager import model_manager
import asyncio

bp = Blueprint('deepclaude', __name__, url_prefix='/deepclaude')


# 生成图片表单提交功能接口，测试用的
@bp.route('/v1/chat/completions', methods=['POST'])
async def completions():
    body =  await asyncio.to_thread(request.get_json, force=True)
    # 创建任务，并直接返回，服务端通过多线程方式实现多任务
    return await model_manager.process_request(body)
