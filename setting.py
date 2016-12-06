#!/usr/bin/env python
import os
import json
import redis
#EXEC = os.getenv("THHT_EXEC" , None)
#if not EXEC :
#    raise Exception("Error : have not set the exec ! ")
#EXEC = "/HOME/nscc-gz_jiangli/virtualenv/ht_celery/simtask.py"
#WDIR = "/HOME/nscc-gz_jiangli/virtualenv/ht_celery"
#INPUT = os.getenv( "THHT_INPUT", "input.htc"  )
#AUTONAME = "True"
thht_port = int( os.getenv( "THHT_PORT", 6379  ) )
thht_host = os.getenv( "THHT_HOST", None  )
if not thht_host :
    print( " Not set THHT_HOST ")
    raise Exception("Not set THHT_HOST ! ")
with open("settings.json") as infile :
    settings = json.load(infile)
print ( thht_host , thht_port  )
r =  redis.Redis( host= thht_host , port = thht_port ) 
r.set('htth-settings' , json.dumps( settings )  )
## json.loads( jj.decode('utf-8') )
print ( "set settings to redis ready ! ") 
