from __future__ import absolute_import ,unicode_literals

import os

from celery import Celery, Task
import redis , json


thht_port = int( os.getenv( "THHT_PORT", 6379  ) )
thht_host = os.getenv( "THHT_HOST", None  )
if not thht_host :
    raise Exception("Error: No THHT_HOST SET")
r = redis.Redis( host= thht_host , port = thht_port ) 
settings = json.loads( r.get('htth-settings'  ).decode('utf-8') ) 


masterip = os.environ["THHT_HOST"]
thht_port = str( os.getenv( "THHT_PORT", 6379  ) )

masterip = masterip + ':' + thht_port

app = Celery('ht_celery' ,
          broker="redis://" + masterip,
          backend="redis://"  + masterip,
          include = ['ht_celery.tasks'] )

app.conf.update(
    result_expires = 3600 ,
    result_serializer = "pickle" , 
    accept_content = ['pickle' , 'json']
)

if __name__ == '__main__':
    app.start()
