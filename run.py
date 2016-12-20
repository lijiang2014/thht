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
filename = "task_state"
pathname = "%s/%s" % (path, filename)
print (path, pathname)
task_list = []
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
        task_list.append(task_info)
rs = ResultSet( results )
print( rs.get( propagate = False ) ) 

success_task_id = []
success_list = r.lrange('success_list', 0, r.llen('success_list') - 1)
fail_list = r.lrange('fail_list', 0, r.llen('fail_list') - 1)
# remove duplicate
success_list = list(set(success_list))
fail_list = list(set(fail_list))
# task info joint
for success_task in success_list:
	success_task = eval(success_task)
	task_id = success_task['task_id']
	task_retval = success_task['retval']
	success_task_id.append(task_id)
	for i in range(0, len(task_list)):
		if task_id == task_list[i]['task_id']:
			task_list[i]['state'] = 'success'
			task_list[i]['retval/exc'] = task_retval
for fail_task in fail_list:
	fail_task = eval(fail_task)
	task_id = fail_task['task_id']
	task_exc = fail_task['exc']
	if fail_task['task_id'] in success_task_id:
		continue
	else:
		for i in range(0, len(task_list)):
			if task_id == task_list[i]['task_id']:
				task_list[i]['state'] = 'fail'
				task_list[i]['retval/exc'] = task_exc
# get task state from redis
keys = ['task_id', 'task_name', 'task_cmd', 'state', 'retval/exc']
with open(pathname, 'a') as f:
	for task in task_list:
		print (task)
		record_items = []
		record = ''
		for key in keys:
			record_items.append(str(task[key]))
		record_items.append('\n')
		record = ' '.join(record_items)
		print (record)
		f.write(record)
