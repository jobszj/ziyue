import concurrent.futures

class ThreadPoolSingleton:
    _instance = None

    def __new__(cls, max_workers=10):
        if cls._instance is None:
            cls._instance = super(ThreadPoolSingleton, cls).__new__(cls)
            cls._instance.executor = concurrent.futures.ThreadPoolExecutor(max_workers=max_workers)
        return cls._instance

    def get_executor(self):
        return self.executor

# 获取线程池实例的函数
def get_thread_pool_executor():
    return ThreadPoolSingleton().get_executor()