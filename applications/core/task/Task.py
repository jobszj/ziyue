import json

from flask import current_app
from redis import Redis

class Task:
    def __init__(self, queue_name):
        self.queue_name = queue_name
        self.redis_client = Redis.from_url(current_app.config['REDIS_URL'])

    def enqueue(self, task):
        """将任务放入队列"""
        task_json = json.dumps(task)
        with current_app.app_context():
            self.redis_client.rpush(self.queue_name, task_json)

    def dequeue(self):
        """从队列中取出任务"""
        with current_app.app_context():
            task_json = self.redis_client.lpop(self.queue_name)
        if task_json:
            return json.loads(task_json)
        return None

    def remove_task(self, task):
        """从队列中移除任务"""
        task_json = json.dumps(task)
        with current_app.app_context():
            self.redis_client.lrem(self.queue_name, 0, task_json)

