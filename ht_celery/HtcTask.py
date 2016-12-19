import os
import redis
from celery import Task

class HtcTask(Task):

    def __init__(self):
     
        thht_port = int( os.getenv( "THHT_PORT", 6379  ) )
        thht_host = os.getenv( "THHT_HOST", None  )
        if not thht_host :
            raise Exception("Error: No THHT_HOST SET")
        self.redis_instance = redis.Redis( host= thht_host , port = thht_port ) 

    def on_success(self, retval, task_id, args, kwargs):
        task_info = {'task_id': task_id,
                     'retval': retval,}
        self.redis_instance.lpush('success_list', task_info)

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        task_info = {'task_id': task_id,
                     'exc': exc}
        self.redis_instance.lpush('fail_list', task_info)

    def on_retry(self, exc, task_id, args, kwargs, einfo):
        task_info = {'task_id': task_id,
                     'exc': exc}
        self.redis_instance.lpush('retry_list', task_info)