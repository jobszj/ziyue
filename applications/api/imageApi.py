# 示例 API 路由
from flask import Blueprint
from applications.core.task.Task import add_task_to_queue

api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/hello', methods=['GET'])
def hello():
    task = {"task_id": 11, "data": "example data"}
    add_task_to_queue(task)
    return "Task enqueued"

