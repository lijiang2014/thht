#!/usr/bin/env python
from setting import *
from celery import group
from ht_celery.tasks import run_command
from celery.result import ResultSet
USE_NAME = True
f = open(INPUT , "r")
results = []
#record = {}
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
rs = ResultSet( results )
rs.get()
