from __future__ import absolute_import ,unicode_literals

import os

from celery import Celery

masterip = os.environ["THHT_HOST"]
thht_port = str( os.getenv( "THHT_PORT", 6379  ) )

masterip = masterip + ':' + thht_port

app = Celery('ht_celery' ,
          broker="redis://" + masterip,
          backend="redis://"  + masterip,
          include = ['ht_celery.tasks'] )

app.conf.update(
    result_expires = 3600 ,
)

if __name__ == '__main__':
    app.start()
