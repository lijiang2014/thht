from __future__ import absolute_import ,unicode_literals

import os

from celery import Celery

masterip = os.environ["HT_CELERY_IP"]

app = Celery('ht_celery' ,
          broker="redis://" + masterip,
          backend="redis://"  + masterip,
          include = ['ht_celery.tasks'] )

app.conf.update(
    result_expires = 3600 ,
)

if __name__ == '__main__':
    app.start()
