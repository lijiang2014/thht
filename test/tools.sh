#!/bin/sh
export THHT_PATH=/WORK/app/thht
export THHT_PACKAGE_PATH=$THHT_PATH/thht
export PATH=$THHT_PATH/bin:$THHT_PATH/thht:$PATH
export LD_LIBRARY_PATH=$THHT_PATH/lib:$LD_LIBRARY_PATH
export PYTHON_PATH=$THHT_PACKAGE_PATH
/WORK/app/thht/thht/tools.py $@
