#!/bin/bash
# run this main shell on the head node .
# MAX TIME must be set.
date
TIME_LIMITE=30
export THHT_HOST=$HOSTNAME
echo $THHT_HOST

#THHT_PATH
export OLD_PATH=$PATH
export OLD_LD_LIBRARY_PATH=$LD_LIBRARY_PATH
export OLDPYTHONPATH=$PYTHONPATH
export PATH=$THHT_PATH/bin:$THHT_PATH/thht:$PATH
export LD_LIBRARY_PATH=$THHT_PATH/lib:$LD_LIBRARY_PATH
export PYTHONPATH=$THHT_PATH/thht:$PYTHONPATH
######################################
# HT_CELERY_DIR = 
# REDIS_DIR = 


# make config server 
config.py $@
# run redis-server 
nohup /WORK/app/redis/3.2.4/bin/redis-server ./redis.conf &> log.redis &
###  check the redis-server is OK and put the settings into redis .
sleep 1 
setting.py



### read the settings.htc file and write settings to redis DB . 

# setting.py $@





# run workers 

## This line only for one machine debug 



##

 
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
