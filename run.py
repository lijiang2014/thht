#!/usr/bin/env python
#from setting import *
import redis , json
from celery import group
from ht_celery.tasks import run_command
from celery.result import ResultSet
import os
USE_NAME = True
thht_port = int( os.getenv( "THHT_PORT", 6379  ) )
thht_host = os.getenv( "THHT_HOST", None  )
r = redis.Redis( host= thht_host , port = thht_port ) 
settings = json.loads( r.get('htth-settings'  ).decode('utf-8') ) 
EXEC = settings["job"]["exec"] 
f = open( settings["job"]["input"] , "r")
results = []
#record = {}
path = os.getcwd()
for line in f :
    if line.strip():
        if USE_NAME :
            ( tname , targs ) = line.strip().split(' ',1 )
        else :
            targs = line 
        cmd = " ".join( [ EXEC ,  targs ])    
        print( cmd )
        rest = run_command.delay(cmd )
        results.append(rest)
        # record task info
        task_info = {}
        task_info['task_name'] = tname
        task_info['task_cmd'] = cmd
        task_info['task_id'] = rest.task_id
        r.lpush('tasks_info', task_info)
rs = ResultSet( results )
print( rs.get( propagate = False ) ) 

r.save
print 'finish'
