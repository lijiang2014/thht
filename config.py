#!/usr/bin/env python
import os
import socket
import sys
import json
#class Settings(object):
#    def __init__(self):
#        self.name = 'ht_celery'
#        self.port = 6379
#        self.workdir = os.getcwd()
#        self.ip = socket.gethostname()
#settings = Settings()

settings = {
    "name" : 'ht_celery' ,
    "port" : 6379,
    "workdir" : os.getcwd(),
#   "ip" : socket.gethostname(),
    "job" : {     # settings for this HT job 
        "exec" : None ,
        "input" : "input.htc" ,
        "autoname" : True ,  # from [ "Auto" , "Set"  ]
        "autoworkdir" :  True ,    # from [ ]
        "env" : "pass" , # from [ "bash" , "pass" ]
    },
    "queue" : {   # Celery queue task 
        "default_retry_delay" : 1 ,
        "max_retries" : 3 ,
        "retry_retcode" : False ,
        "retry_exception" : True ,
        "rate_limit" : None,
        "time_limit" : None,
        "soft_time_limit" : None , 
    },
}

def JSONvalue(value , jtype = [ "bool" , "none" , "num" , "str" ] ):
    val = value.lower()
    if val in [ "true" , "yes" ] and "bool" in jtype :
        return True
    elif val in [ "false" , "no" ] and "bool" in jtype :
        return False 
    elif val in [ "none" , "non" , "null"  ] and "none" in jtype :
        return None 
    elif val.isdigit() and  "num" in jtype :
        return int(val)
    if "str" not in jtype :
        raise Exception("Error SETTINGS TYPE ." , value )
    return value




print( sys.argv )
if len(sys.argv) > 1 :
    ''' read setting from file  '''
    sf = open( sys.argv[1])
    for eachLine in sf:
        print( eachLine )
        data = eachLine.split('=' , 1)
        if len( data ) == 2 :
            sname = data[0].strip().lower()
            svalue = data[1].strip()
            if sname.startswith('#') :
                continue
            if sname.lower() in [  "exec" ] :
                settings["job"]["exec"] = svalue
            elif sname in [   "input" ,  "inp" ] :
                settings["job"]["input"] = svalue
            elif sname in [   "name" ,  "autoname" ] :
                settings["job"]["autoname"] = JSONvalue( svalue , jtype = [ "bool" ]   )
            elif sname in [   "dir" ,  "workdir" , "autoworkdir" ] :
                settings["job"]["autoworkdir"] = JSONvalue( svalue , jtype = [ "bool" ]   )
            else :
                snamed = sname.split('.' , 1)
                if len( snamed ) == 2 :
                    [ sname_p1 , sname_p2 ] = snamed
                else :
                    [ sname_p1 , sname_p2 ] = [ "queue"  ,sname ]
                if sname_p1 in settings.keys() and sname_p2 in settings[sname_p1 ].keys() :
                    settings[ sname_p1 ][ sname_p2 ] = JSONvalue( svalue )
                else :
                    print( " WARING : NO SUCH SETTING : " , eachLine )
    sf.close()
else : # No SETTINGS FILE 
    settings["job"]["exec"]  = os.getenv("THHT_EXEC" , None)
    if not settings["job"]["exec"]  :
        raise Exception("Error : have not set the exec ! ")
    settings["job"]["input"] = os.getenv( "THHT_INPUT", "input.htc"  )

# 

# write settings to json file 

with open( "settings.json" , "w" ) as outfile :
    json.dump( settings , outfile )


# settings.ip 
# settings.port , settings.workdir 



# create redis.config
redis_config_str = '''
bind %s  
# redis ip
protected-mode yes  
# 
port %s 
# port default 6379
timeout 0
tcp-keepalive 300
daemonize no
supervised no
#pidfile /var/run/redis_6379.pid
pidfile %s
save 900 1
save 300 10
save 60 100000
stop-writes-on-bgsave-error yes
rdbcompression yes
dbfilename dump.rdb
dir ./
slave-serve-stale-data yes
 maxclients 4064
# 
'''

redis_config = redis_config_str %  ( socket.gethostname()  , settings["port"] , settings["workdir"] +'/redis.pid' ) 

f = open( 'redis.conf' , 'w' )
f.write( redis_config )
f.close()


#EXEC = "/HOME/nscc-gz_jiangli/virtualenv/tmptest/simtask.py"
#WDIR = "/HOME/nscc-gz_jiangli/virtualenv/tmptest"
#INPUT = "input.htc"
#AUTONAME = "True"
