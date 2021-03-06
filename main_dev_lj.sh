#!/bin/bash
# run this main shell on the head node .
# MAX TIME must be set.
date
TIME_LIMITE=30
export THHT_HOST=$HOSTNAME
echo $THHT_HOST
export THHT_PYTHON_PATH=$THHT_PATH/bin
export THHT_PYTHON_LIB=$THHT_PATH/lib
export THHT_PACKAGE_PATH=$THHT_PATH/thht
export THHT_REDIS_PATH=/WORK/app/redis/3.2.4/bin
#THHT_PATH
export OLD_PATH=$PATH
export OLD_LD_LIBRARY_PATH=$LD_LIBRARY_PATH
export OLDPYTHONPATH=$PYTHONPATH
export PATH=$THHT_PYTHON_PATH:$THHT_PACKAGE_PATH:$PATH
export LD_LIBRARY_PATH=$THHT_PYTHON_LIB:$LD_LIBRARY_PATH
export PYTHONPATH=$THHT_PACKAGE_PATH
######################################


# make config server 
config.py $@
# run redis-server 
nohup $THHT_REDIS_PATH/redis-server ./redis.conf &> log.redis &
###  check the redis-server is OK and put the settings into redis .
sleep 1 
setting.py

#echo " srun -N $[ SLURM_NNODES - 1 ] -n $[ SLURM_NNODES - 1 ]  -x $THHT_HOST  "
#srun -N $[ SLURM_NNODES - 1 ] -n $[ SLURM_NNODES - 1 ]  -x $THHT_HOST celery -A ht_celery worker -l info &> log.worker &

srun -N $[ SLURM_NNODES  ] -n $[ SLURM_NNODES  ] -c 24 --no-kill -W 9999999 run_thht_worker.sh &  # -x $THHT_HOST celery -A ht_celery worker -l info &> log.worker &

## wait

## PUT JOB INTO QUEUE 
#sleep 10

run.py  &> log.run &

monitor.py

#wait 

## WAIT TASK RUN
### sleep $TIME_LIMITE 

## EXITS 
killall -9 redis-server &> /dev/null
killall -9 celery &> /dev/null
killall -9 python3 &> /dev/null
date
