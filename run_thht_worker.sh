#!/bin/sh
myhost=`hostname`
if [[ s$myhost = s$THHT_HOST ]] ; then
 echo "OK"
 #  celery -A ht_celery worker -l info &>> log.worker &
fi
