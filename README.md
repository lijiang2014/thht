# for a simle HT-JOB , you can : 

time ( cat input.htc  | xargs -i -P 24 ./simtask.py {} ) 

# Test the celery task 

cd test 

./test.sh

# In this local env , u need do some changes , please see the wiki: local test


Analysize.py report task state
usage:		python analysize.py [-n|-h]
            -n      task name
            -h      help