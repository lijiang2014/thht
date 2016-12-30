from celery import Task
import time , json
class HtcTask(Task):
    
    def on_success(self, retval, task_id, args, kwargs):
        #task_info = {'task_id': task_id,
        #             'retval': retval,}
        self.backend.client.lpush('success_list', task_id)
        self.backend.client.hdel( 'thht_id_pd' , task_id  )
        key = 'celery-task-meta-%s' % task_id
        self.backend.client.delete(key)

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        self.backend.client.lpush('fail_list', task_id) # == hkeys('fail_log')
        self.backend.client.hdel( 'thht_id_pd' ,  task_id  )
        #self.backend.client.hmset( 'thht_id_pd' , { rest.task_id : 'F' })
        self.logError( exc, task_id, args, kwargs, einfo)
        key = 'celery-task-meta-%s' % task_id
        self.backend.client.delete(key)

    def on_retry(self, exc, task_id, args, kwargs, einfo):
        pass
        num = self.backend.client.lpush('retry_list', task_id)
        # TO-DO exc may be huge , need to check !
        self.backend.client.hincrby('thht_exc_log',  exc )
        # TO-DO if log_retry , not safty , may need a lot of mem ! 
        self.logError( exc, task_id, args, kwargs, einfo)        
    def logError(self , exc , task_id ,args, kwargs, einfo):
        err_info = {
            'task_id' : task_id ,
            'exc' : str(exc) ,
            #'einfo' : einfo ,
            'date' : time.time() ,
            'host' : self.request.hostname ,
        }
        self.backend.client.lpush('err_log', json.dumps(err_info))
    
