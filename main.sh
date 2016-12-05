#!/bin/bash
# run this main shell on the head node .
# MAX TIME must be set.
date
TIME_LIMITE=30
export HT_CELERY_IP=$HOSTNAME
echo $HT_CELERY_IP
# make config server 
config.py
# run redis-server 
nohup /WORK/app/redis/3.2.4/bin/redis-server ./redis.conf &> log.redis &
### echo $TIME_LIMITE
# run workers 

## This line only for one machine debug 

yhrun -N $SLURM_NNODES -n $SLURM_NNODES  celery -A ht_celery worker -l info &> log.worker &

## wait

## PUT JOB INTO QUEUE 
#sleep 10

 run.py  &> log.run

#wait 
#sleep 10000

## WAIT TASK RUN
### sleep $TIME_LIMITE 

## EXITS 
killall -9 redis-server &> /dev/null
killall -9 celery &> /dev/null
killall -9 python3 &> /dev/null
date
