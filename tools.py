#!/usr/bin/env python
from __future__ import absolute_import , unicode_literals

import os
import sys
import json , redis 
from getopt import getopt, GetoptError
from subprocess import Popen, PIPE
from celery.result import AsyncResult
from ht_celery.celery import app

class Client(object):
    def __init__(self):
        with open("settings.json") as infile :
            settings = json.load(infile)
            r =  redis.Redis( host= settings['job']['host'] , port = settings['port'] )
        try :
            r.client_getname()
            state = "net"
        except Exception as ex :
            state = "file"
        self.state = state
        self.r = r
        self._all = None
        self._summary = None
        self._thht_id_name = {}
        self._thht_name_id = {}
    def end(self):
        self.r.set( "thht_state" , "ALL PUSHED" )
    def kill(self):
        self.r.set( "thht_kill" , "KILL" )
    def summary(self , retry = False ) :
        if self.state == "net" :
            r = self.r
            result = {
                'tasks' : r.hlen('thht_id_name') ,
                'success' : r.llen('success_list' ) ,
                'failure' : r.llen('fail_list') ,
            #    'retry'   : r.llen('retry_list') 
            }
            if retry :
                result["retry"] = r.llen('retry_list')
        return result
    def success(self , isHum=False ):
        if self.state == "net" :
            r =self.r
            result = r.lrange('success_list' , 0 , -1)
            if isHum :
                result = self.get_name_by_id( result  , encode = None)
        return result
    def failure(self ,isHum=False ):
        if self.state == "net" :
            r = self.r
            result = r.lrange('fail_list' , 0 , -1)
            if isHum :
                result = self.get_name_by_id( result  , encode = None)
            return result
    def pd(self):
        if self.state == "net" :
            result = self.r.llen('celery')
        return result
    def running(self):
        if self.state == "net" :
            from ht_celery.celery import app
            from  celery.bin.control import inspect            
            #result = inspect( app=app ,  quiet=True  ).run_from_argv('celery', ['active', '-A', 'ht_celery'], command='inspect')
            result = app.control.inspect(  )._request(  'active' )
        return result
    #def retry(self , isHum=False):
    #    if self.state == "net" :
    #        result = self.r.lrange('retry_list' ,0 , -1)
    #        if isHum :
    #            result = self.get_name_by_id( result  , encode = None)            
    #    return result
    def tasks(self):
        if self.state == "net" :
            result = self.r.hgetall('thht_id_info' )
        return result
    def get_name_by_id(self,id , encode = ' utf-8') :
        if self.state == "net":
            pass
            if self.r.hlen( 'thht_id_name') != len( self._thht_id_name) :
                self._thht_id_name = self.r.hgetall('thht_id_name' )
            if isinstance( id  ,list) :
                if encode :
                    name = [ self._thht_id_name[ idi.encode( encode )  ] for idi in id ]
                else :
                    name = [ self._thht_id_name[ idi ] for idi in id ]
            else :
                name = self._thht_id_name[ id.encode('utf-8')  ]
            return name
    def task_name(self , name) :
        if self.state == "net" :
            id = self.r.hget('thht_name_id', name)
            result = {}
            self.all()
            status = "unkown"
            info = ""
            if id in self._all["success"] :
                status = "SUCCESS"
            elif id in self._all["failure"] :
                status = "FAILURE"
            else :
                ar = AsyncResult(id)
                status = ar.state
            result["id"] = id
            result["status"] = status
            result["info"] = info
        return result
    def all(self , retry = False ):
        if self.state == "net" :
            r =self.r
            summary = self.summary()
            if self._summary != summary : # All just update appends
                result = {
                  'tasks' : self.tasks(),
                  'success' : self.success() ,
                  'failure' : self.failure() ,
                  #'retry'   : self.retry() 
                }
                #if retry : result["retry"] = self.retry() 
                self._all = result
                self._summary = {
                   'tasks' : len( result['tasks']  ) ,
                   'success' : len( result['success'] ) ,
                   'failure' : len( result['failure']),
                #   'retry'   : len( result['retry'] )
                }
                #if retry : self._summary["retry"] = len( result['retry'] )
            else :
                result = self._all
        return result
    def error(self, isHum=False):
        if self.state == "net" :
            result = self.r.lrange('err_log',0,-1)
        if isHum :
            newresult = []
            for item in result :
                data = json.loads( item.decode('utf-8'))
                task_name = self.get_name_by_id( data["task_id"] )
                data["task_name"] = task_name
                newresult.append(data)
            result = newresult
        return result
    def job_name(self , name):
        print("Not Imp Yet")






def usage():
    print ('''usage:      analysize [-n|-h|-e]
            -s | --summary get a summary info
            -e | --end end job push.
            -h      help''')
    exit(1)

def format_print( data , summ = True , isHum = False , indence = 2 ):
    if not isHum :
        print( data )
        return None
    if isinstance(data , bytes) :
        data = data.decode('utf-8')
    #if isinstance(data ,str)
    #if isinstance(data , bytes) :
    #    data = data.decode('utf-8')
        
    if isinstance(data , list ):
        #print ("List : ")
        #print( data )
        print('%s [' % (' '*indence) )
        for item in data :
            #if isinstance(item , bytes ) :
            #    item = item.decode('utf-8')
            format_print( item , summ=summ , isHum=isHum , indence = indence +2 )
        print('%s ]' % (' '*indence) )        
    elif isinstance( data, dict ):
        #print("Dict :")
        print('%s {' % (' '*indence) )
        for (key , value) in data.items() :
            if isinstance(value , bytes ) :
                value = value.decode('utf-8')
            if isinstance(value, (int , float  )) :
                value = str(value)
            if isinstance(value , str ) :
                print('%s   %s  :  %s' % (' '*indence , key , value ) )
            else :
                print('%s   %s  :' % (' '*indence , key  ) )
                format_print( value , summ=summ , isHum=isHum , indence = indence +2 )
        print('%s }' % (' '*indence) )
    else :
        print('%s   %s' % (' '*indence , data  ) )
        count = False
    #print('num count : %d' % len(data))

if __name__ == '__main__':
    c = Client()
    try:
        opts, args = getopt(sys.argv[1:], "hn:sekrSRPFEH", ["task_name=", "help" , "summary","end", "Success" ,"Running", "Pendding", "Failure", "kill","Error"] )
        if len(opts) == 0:
            print ('Not Imp Yet')
        else:
            isretry = ('-r','') in opts
            isHum = ('-H','') in opts
            for opt, argv in opts:
                print( 'o ,a :' , opt , argv)
                if opt in ('-h', "--help"):
                    usage()
                elif opt in ('-s', "--summary"):
                    print( "Summary (-s) :" )
                    data = ( c.summary( retry = isretry ) )
                    format_print( data , isHum= isHum )
                elif opt in ('-e', "--end"):
                    c.end()
                elif opt in ('-k', "--kill"):
                    c.kill()
                elif opt in ('-S', "--Success"):
                    print( "Success Tasks (-S) :" )
                    data = c.success(isHum= isHum )
                    format_print( data , isHum= isHum )
                elif opt in ('-F', "--Failure"):
                    print( "Failure Tasks (-F) :" )
                    data = c.failure( isHum= isHum)
                    format_print( data , isHum= isHum )
                elif opt in ('-R', "--Running"):
                    print( "Running Tasks (-R) :" )
                    data = c.running()
                    format_print( data , isHum= isHum )
                elif opt in ('-P', "--Pendding"):
                    print( "Pendding Tasks (-S) :" )
                    data = c.pd(isHum= isHum )
                    format_print( data , isHum= isHum )
                elif opt in ('-E', "--Error"):
                    print( "Task Errors (-E) :" )
                    data = c.error(isHum=isHum)
                    format_print( data , isHum= isHum )
                elif opt in ('-n', "--task_name"):
                    print( "Task info (-n) :" )
                    data = c.task_name( argv)
                    format_print( data , isHum= isHum )
                else:
                    pass
    except GetoptError:
        usage()
