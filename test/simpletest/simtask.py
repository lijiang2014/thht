#!/usr/bin/env python
import time
import random
import sys
error_r = 0.0  # return code not 0
error_exception = 0.0  # raise Exception
time_run = 30
taskrad = random.random()
time.sleep( 1 )
print (str(sys.argv))
if len( sys.argv ) > 1  and sys.argv[1] == 'e' : # case always error . 
    print('Error case ')
    raise Exception( "Error case ! " )
if taskrad <= error_r :
    print ('Error by Error radio')
    exit( 500 )
if taskrad <= error_exception :
    print ('Error by Exception')
    raise Exception( "test exception " )
    exit(600)
else :
    #time_run  += random.normalvariate( 1 , 1 )
    time.sleep( time_run )
    print ('Run END OK')
    exit


