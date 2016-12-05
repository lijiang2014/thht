#!/usr/bin/env python
import os
import socket

class Settings(object):
    def __init__(self):
        self.name = 'ht_celery'
        self.port = 6379
        self.workdir = os.getcwd()
        self.ip = socket.gethostname()
settings = Settings()

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
save 60 10000
stop-writes-on-bgsave-error yes
rdbcompression yes
dbfilename dump.rdb
dir ./
slave-serve-stale-data yes
 maxclients 4064
# 
'''

redis_config = redis_config_str %  ( settings.ip , settings.port , settings.workdir +'/redis.pid' ) 

f = open( 'redis.conf' , 'w' )
f.write( redis_config )
f.close()


#EXEC = "/HOME/nscc-gz_jiangli/virtualenv/tmptest/simtask.py"
#WDIR = "/HOME/nscc-gz_jiangli/virtualenv/tmptest"
#INPUT = "input.htc"
#AUTONAME = "True"
