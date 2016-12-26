#!/usr/bin/env python
import redis , json
import os , time , sys
print ("Hello monitor")
USE_NAME = True
thht_port = int( os.getenv( "THHT_PORT", 6379  ) )
thht_host = os.getenv( "THHT_HOST", None  )
r = redis.Redis( host= thht_host , port = thht_port )

isAllPushed = ( r.get( "thht_state" ) == "ALL PUSHED" )
print( 'thht_state ' , r.get( "thht_state" )   )
while  True : 
    sys.stdout.flush()
    sln = r.llen('success_list')
    fln = r.llen('fail_list')
    if not isAllPushed :
        isAllPushed = r.get( "thht_state" )
        isAllPushed = False if isAllPushed is None else isAllPushed.decode('utf-8') == "ALL PUSHED"
        #isAllPushed = ( (r.get( "thht_state" )).decode('utf-8') == "ALL PUSHED" )
        if isAllPushed  :
            print( "All Pushed" )
        #print( 'thht_state ' , (r.get( "thht_state" ).decode('utf-8')))  
    aln = r.llen('tasks_info')
    if (( aln == (sln + fln)  ) and  aln >0 and isAllPushed is True ) :
        print('End?a , s, f, is ' , aln , sln , fln , isAllPushed  )
        break
    time.sleep( 1  )
    
print( 'A :', r.llen('tasks_info'))
print( 'S :', r.llen('success_list') )
print( 'F :', r.llen('fail_list'))
print( 'R :', r.llen('retry_list'))
r.save()
print ('finish')

