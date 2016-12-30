#!/usr/bin/env python
#from setting import *
import redis , json
from celery import group
from ht_celery.tasks import run_command
from celery.result import ResultSet
import os , time
ISOTIMEFORMAT='%Y-%m-%d %X'
class RunClient( object ) :
    def __init__(self , host , port ):
        self.r = redis.Redis( host= host , port = port )
        self.settings = json.loads( self.r.get('thht_settings'  ).decode('utf-8') ) 
        self.USE_NAME = True
    def runlevel(self) : 
        return int(os.getenv( "THHT_RUN_LEVEL", 0  ))
    def smartStart(self):
        # if state = stare just read JobFile
        if self.r.get("thht_state" ) == b"STARE" :
            print("First Run")
            self.readJobFile()
        else :  # retry ,  all data in db ?
            print("restare Run")
            jobsindb = self.r.hlen( 'thht_id_info' )
            jobsinfile = self.wcJobFile()
            if jobsindb == jobsinfile :
                print("data already in dbs") # but data may not in PD queue <r-celery>
                self.runDBJob()
                # this is better to do in setting part . 
                # same job may lost , but could be recover from  bd?
                pass # nothing need to do ? May do somting  TO-DO
            else :
                print("Not Done Yet . Need to read files to decide . ")
        if self.runlevel() == 0 :
            self.r.set( "thht_state" , "ALL PUSHED" )

    def runDBJob(self):
        # recreate job and refresh  info
        dbjobs = self.r.hgetall('thht_id_pd')
        for tid , tst in dbjobs.items():
            if tst == b'pd' :
                task_info = json.loads( self.r.hget("thht_id_info" , tid ).decode('utf-8') )
                rest =    run_command.delay( task_info[ 'task_cmd' ] )
                task_info[ 'task_id'] = rest.task_id
                # create new db infos 
                self.r.hmset( 'thht_id_name' , { rest.task_id : task_info[ 'task_name']  } )
                self.r.hmset( 'thht_id_info' , { rest.task_id : json.dumps(task_info) })
                self.r.hmset( 'thht_name_id' , { task_info[ 'task_name']  : rest.task_id} )
                self.r.hmset( 'thht_id_pd' , { rest.task_id : 'pd' })
                # clean old db infos
                self.r.hdel( 'thht_id_name'  ,  tid )
                self.r.hdel( 'thht_id_info'  ,  tid )
                self.r.hdel( 'thht_id_pd'  ,  tid )
                # DEL  'thht_id_name' may course some problem ? 
                # not del 'thht_id_name' may course others problem ?
                pass
        pass
         
    
    def wcJobFile(self , filename = None) :
        count = 0;
        if filename is None :
            filename = self.settings["job"]["input"]
        f = open( filename , "r")
        for line in f :
            count += 1 
        return count
        
    def readJobFile( self , filename = None) :
        if filename is None :
            filename = self.settings["job"]["input"] 
        EXEC = self.settings["job"]["exec"] 
        f = open( filename , "r")
        for line in f :
            if line.strip():
                if self.USE_NAME :
                    ( tname , targs ) = line.strip().split(' ',1 )
                else :
                    targs = line 
                cmd = " ".join( [ EXEC ,  targs ])    
                print( cmd )
                rest =    run_command.delay(cmd )
                #results.append(rest)
                task_info = {}
                task_info['task_name'] = tname
                task_info['task_cmd'] = cmd
                task_info['task_id'] = rest.task_id
                task_info = json.dumps(task_info)
                self.r.hmset( 'thht_id_name' , { rest.task_id : tname } )
                self.r.hmset( 'thht_id_info' , { rest.task_id : task_info })
                self.r.hmset( 'thht_name_id' , {tname : rest.task_id} )
                self.r.hmset( 'thht_id_pd' , { rest.task_id : 'pd' })
                

        
if __name__ == '__main__' :
    print('run.py')
    print( time.strftime( ISOTIMEFORMAT, time.localtime() ) )
    thht_port = int( os.getenv( "THHT_PORT", 6379  ) )
    thht_host = os.getenv( "THHT_HOST", None  )
    rc  = RunClient( host = thht_host , port = thht_port )
    #rc.readJobFile()
    rc.smartStart()
    #print( "all job from file pushed" )
    #if rc.runlevel() == 0 :
    #    rc.r.set( "thht_state" , "ALL PUSHED" )
    print( "set " , rc.r.get( "thht_state" ) , "time : " , time.strftime( ISOTIMEFORMAT, time.localtime() ) )
    #print( "len tasks info" ,     r.llen('tasks_info'))

    
#USE_NAME = True
#settings = json.loads( r.get('thht_settings'  ).decode('utf-8') ) 
#EXEC = settings["job"]["exec"] 
#f = open( settings["job"]["input"] , "r")
#results = []
#path = os.getcwd()


