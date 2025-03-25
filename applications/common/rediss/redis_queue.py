from flask import current_app
import redis
import hashlib

# 定义任务状态
TASK_STATUS_PENDING = 'pending'
TASK_STATUS_PROCESSING = 'processing'
TASK_STATUS_COMPLETED = 'completed'

def get_redis_client():
    return redis.from_url(current_app.config['REDIS_URL'])


def add_task_to_queue(task):
    redis_client = get_redis_client()
    # 计算任务的哈希值
    task_hash = hashlib.sha256(str(task).encode()).hexdigest()
    # 检查任务是否已存在
    if redis_client.sadd('image_task', task_hash):
        # 任务不存在，添加到队列
        redis_client.rpush("image_queue", task)
        # 初始化任务状态为 pending
        redis_client.hset('task_status', task_hash, TASK_STATUS_PROCESSING)
        return True
    return False


def get_next_task():
    redis_client = get_redis_client()
    task = redis_client.lpop('image_task')
    if task:
        task = task.decode()
        task_hash = hashlib.sha256(str(task).encode()).hexdigest()
        # 更新任务状态为 processing
        redis_client.hset('task_status', task_hash, TASK_STATUS_PROCESSING)
        return task
    return None


def mark_task_completed(task):
    redis_client = get_redis_client()
    task_hash = hashlib.sha256(str(task).encode()).hexdigest()
    # 更新任务状态为 completed
    redis_client.hset('task_status', task_hash, TASK_STATUS_COMPLETED)
