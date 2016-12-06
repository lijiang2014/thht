src_path=/HOME/nscc-gz_jiangli/virtualenv/ht_celery
export PATH=$src_path:$PATH
export THHT_EXEC="/HOME/nscc-gz_jiangli/virtualenv/ht_celery/simtask.py"
export THHT_INPUT="input.htc"
yhbatch -N 2 $src_path/main.sh settings.htc
