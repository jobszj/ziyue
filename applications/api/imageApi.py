# 示例 API 路由
from flask import Blueprint
from applications.core.task.Task import enqueue, dequeue

api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/hello', methods=['GET'])
def hello():
    task = {"task_id": 1, "data": "example data"}
    enqueue(11, task)
    return "Task enqueued"

