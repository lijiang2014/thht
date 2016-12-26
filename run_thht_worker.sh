#!/bin/sh
myhost=`hostname`
if [ s$THHT_NODE_WORKER = s ] ; then
  THHT_NODE_WORKER=24
fi
if [ s$THHT_HOST_WORKER = s ] ; then
  THHT_HOST_WORKER=$THHT_NODE_WORKER
fi
if [ s$myhost != s$THHT_HOST ] ; then
 #  echo "OK"
 #  celery -A ht_celery worker --autoscale=24,1  -l info &> log.worker.$myhost &
 celery -A ht_celery worker --concurrency=$THHT_NODE_WORKER  -l info &> log.worker.$myhost 
else
  if [ $THHT_HOST_WORKER -lt 0 ] ; then
   celery -A ht_celery worker --concurrency=$THHT_HOST_WORKER  -l info &> log.worker.$myhost
  fi
fi

