from celery import Task

class HtcTask(Task):

    def on_success(self, retval, task_id, args, kwargs):
        task_info = {'task_id': task_id,
                     'retval': retval,}
        self.backend.client.lpush('success_list', task_info)
        key = "*%s" % task_id
        success_task_key = self.backend.client.keys(key)
        self.backend.client.delete(*success_task_key)

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        task_info = {'task_id': task_id,
                     'exc': exc}
        self.backend.client.lpush('fail_list', task_info)

    def on_retry(self, exc, task_id, args, kwargs, einfo):
        task_info = {'task_id': task_id,
                     'exc': exc}
        self.backend.client.lpush('retry_list', task_info)