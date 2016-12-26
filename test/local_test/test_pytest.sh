#src_path=/HOME/nscc-gz_jiangli/virtualenv/ht_celery
export THHT_PATH=/WORK/app/thht
#export PATH=$THHT_PATH:$PATH
#export THHT_EXEC="/HOME/nscc-gz_jiangli/virtualenv/ht_celery/simtask.py"
#export THHT_INPUT="input.htc"
yhbatch -N 2 $THHT_PATH/thht/main.sh settings_pytest.htc
