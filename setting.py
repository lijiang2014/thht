#!/usr/bin/env python
import os
import json
import redis

thht_port = int( os.getenv( "THHT_PORT", 6379  ) )
thht_host = os.getenv( "THHT_HOST", None  )
if not thht_host :
    print( " Not set THHT_HOST ")
    raise Exception("Not set THHT_HOST ! ")
with open("settings.json") as infile :
    settings = json.load(infile)
r =  redis.Redis( host= thht_host , port = thht_port ) 
r.set('thht_settings' , json.dumps( settings )  )
# clean signals 
if not ( r.get('thht_kill') is None ) :
    r.delete( 'thht_kill' )
thht_run_level = int(os.getenv( "THHT_RUN_LEVEL", 0  ))    
#if thht_run_level >= 1 :
if r.get( "thht_state")  is None :
    r.set("thht_state" , "STARE")
else :
    r.set("thht_state" , "RESTARE")
    r.delete('celery')  # drop celery list , create job from thht_id_pd'

    # push job in queue not finish into a new file  or db ?
    