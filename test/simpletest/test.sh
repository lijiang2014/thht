export THHT_REDIS_PATH=/WORK/app/redis/3.2.4/bin/
export THHT_PATH=/WORK/app/thht
export THHT_PACKAGE_PATH=$THHT_PATH/thht

#export PATH=$THHT_PATH:$PATH
#export THHT_EXEC="/HOME/nscc-gz_jiangli/virtualenv/ht_celery/simtask.py"
export THHT_INPUT="input.htc"
yhbatch -N 2 $THHT_PATH/thht/main.sh settings.htc
