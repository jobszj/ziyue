# 示例 API 路由
from flask import Blueprint
from applications.core.Task import Task

api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/hello', methods=['GET'])
def hello():
    task = {"task_id": 1, "data": "example data"}
    task_queue = Task('my_task_queue')
    task_queue.enqueue(task)
    return "Task enqueued"

@api_bp.route('/dequeue')
def dequeue_task():
    task_queue = Task('my_task_queue')
    task = task_queue.dequeue()
    if task:
        # 处理任务
        result = f"Task processed: {task}"
        # 任务完成后删除
        task_queue.remove_task(task)
        return result
    return "No task in queue"