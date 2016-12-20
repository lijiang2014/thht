#!/bin/sh
myhost=`hostname`
if [[ s$myhost != s$THHT_HOST ]] ; then
 echo "OK"
   celery -A ht_celery worker --autoscale=24,1  -l info &> log.worker.$myhost &
fi
