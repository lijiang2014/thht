#!/usr/bin/env python
import redis , json
import os , time , sys
        

    
class Monitor(object) :
    file_success = '.log.thht.S'
    SUCCESS_LIST = 'success_list'
    FAIL_LIST = 'fail_list'
    ERRLOG_LIST = 'err_log'
    def __init__(self , host , port ):
        self.r = redis.Redis( host= host , port = port )
        self.file_success = '.log.thht.S'
        self.file_failure = '.log.thht.F'
        self.file_error = '.log.thht.E'
        self._fs = open( self.file_success , 'ab+')
        self._fe = open( self.file_error  , 'ab+')
        self._ff = open( self.file_failure , 'ab+')
        self._num_s = self.getnum( self._fs)
        self._num_e = self.getnum( self._fe )
        self._num_f = self.getnum( self._ff )
        self._isAllPushed = False
    def update(self):
        new_len = self.r.llen(Monitor.SUCCESS_LIST)
        if new_len > self._num_s :
            with open( self.file_success , 'a+') as fs:
                for index in range( new_len - self._num_s ):
                    rindex = -1 - index - self._num_s
                    rid = self.r.lindex(Monitor.SUCCESS_LIST, rindex ).decode('UTF-8')
                    rname = self.get_name_from_id( rid )
                    new_line = "%s %s\n" %(rid, rname)
                    fs.write(new_line)
                fs.flush()
                self._num_s = new_len

        new_len = self.r.llen(Monitor.FAIL_LIST)
        if new_len > self._num_f:
            with open( self.file_failure , 'a+') as ff:
                for index in range(new_len - self._num_f):
                    rid = self.r.lindex(Monitor.FAIL_LIST, index).decode('UTF-8')
                    rname = self.get_name_from_id(rid)
                    new_line = "%s %s\n" % (rid, rname)
                    ff.write(new_line)
                ff.flush()
                self._num_f = new_len

        new_len = self.r.llen(Monitor.ERRLOG_LIST)
        if new_len > self._num_e:
            with open( self.file_error , 'ab+') as fe:
                for index in range(new_len - self._num_e):
                    errinfo = eval(self.r.lindex(Monitor.ERRLOG_LIST, index).decode('UTF-8'))
                    try:
                        rname = self.get_name_from_id(errinfo['task_id'])
                        new_line = "%s %s %s %s %s\n" %(errinfo['task_id'], rname, \
                                    errinfo['date'], errinfo['host'], eval(errinfo['exc']))
                        fe.write(bytes(new_line, 'UTF-8'))
                    except KeyError:
                        print ("err log mapping error")
                fe.flush()
                self._num_e = new_len

    def get_name_from_id(self, rid ) :
        name =  self.r.hget('thht_id_name' , rid).decode('UTF-8')
        return name       
        
    def getnum( self , fp ):
        def block(file , size = 65536) :
            while True:
                nb = file.read(size)
                if not nb:
                    break
                yield nb                    
        fplen = fp.tell() 
        if fplen == 0 :
            return 0
        else :
            fp.seek(0,0)
            return sum(line.decode('utf-8').count("\n") for line in block(fp))
    def isAllPushed(self):
        if not self._isAllPushed :
            self._isAllPushed = ( self.r.get( "thht_state" ) == b"ALL PUSHED" )
        return self._isAllPushed
    def wait(self , checktime = 1 ):
        while True :
            if self.isAllPushed() :
                sln = self.r.llen('success_list')
                fln = self.r.llen('fail_list')
                aln = self.r.hlen('thht_id_name')
                if sln + fln == aln :
                    break
            if ( self.r.get("thht_kill") == b"KILL" ) :
                break
            self.update()
            time.sleep( checktime  )
        self.update()
    def summary(self):
        print( 'A :', self.r.hlen('thht_id_name'))
        print( 'S :', self.r.llen('success_list') )
        print( 'F :', self.r.llen('fail_list'))
        print( 'R :', self.r.llen('retry_list'))
    def savedb(self):
        self.r.save()
        
if __name__ == '__main__' :
    print ("Hello monitor")
    thht_port = int( os.getenv( "THHT_PORT", 6379  ) )
    thht_host = os.getenv( "THHT_HOST", None  )
    mon = Monitor( host = thht_host , port = thht_port   )
    mon.wait()
    mon.summary()
    mon.savedb()
    print ('finish')

    #r = redis.Redis( host= thht_host , port = thht_port )
    #isAllPushed = ( r.get( "thht_state" ) == "ALL PUSHED" )
'''
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
    aln = r.hlen('thht_id_name')
    if (( aln == (sln + fln)  ) and  aln >0 and isAllPushed is True ) :
        print('End?a , s, f, is ' , aln , sln , fln , isAllPushed  )
        break
    if ( r.get("thht_kill") == b"KILL" ) :
        break
    time.sleep( 1  )
    
r.save()
'''