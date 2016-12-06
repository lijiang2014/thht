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
r.set('htth-settings' , json.dumps( settings )  )
