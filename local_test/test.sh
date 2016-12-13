#src_path=/HOME/nscc-gz_jiangli/virtualenv/ht_celery
export THHT_PATH=$PWD/../..
export HOSTNAME=localhost
#export PATH=$THHT_PATH:$PATH
#export THHT_EXEC="/HOME/nscc-gz_jiangli/virtualenv/ht_celery/simtask.py"
export THHT_INPUT="input.htc"
bash -c -l " $THHT_PATH/thht/main_local.sh settings.htc "
