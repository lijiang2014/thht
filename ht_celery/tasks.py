from __future__ import absolute_import , unicode_literals

import os
import signal
from subprocess import PIPE, Popen
from ht_celery.HtcTask import HtcTask
from ht_celery.celery import app , settings

@app.task
def add(x,y):
    return x + y

@app.task
def mul(x,y):
    return x * y

@app.task 
def xsum(numbers):
    return sum(numbers)


@app.task(base=HtcTask, bind = True , autoretry_for=(Exception,) , track_started = True , max_retries = settings["queue"]["max_retries"] , default_retry_delay = 1 )
def run_command( self , command, env=None, timeout=600  ):
    env_backup = os.environ.copy()
    if settings["job"]["env"] == "bash" : 
        for i in os.environ.keys() :
            os.unsetenv( i )
        args = [ "bash" , "-c" , "-l" , command ]
    else :
        env_path = os.getenv("OLD_PATH")
        env_ld = os.getenv("OLD_LD_LIBRARY_PATH")
        os.putenv("PATH" , env_path)
        os.putenv("LD_LIBRARY_PATH" , env_ld)
        args = [ "bash" , "-c"  , command ]
    try:
        p = Popen(args, stdout=PIPE, stderr=PIPE, env=env)
    except OSError as  ex:
        #logger.error('running command failed: "%s", OSError "%s"' %(' '.join(args), ex))
        raise self.retry( exc = ex )
    output = ""
    error = ""
    retcode = 0
    signal.alarm(timeout)
    try:
        (output, error) = p.communicate()
        retcode=p.poll()
        signal.alarm(0)  # reset the alarm
    except Exception as ex :
        self.retry(exc= ex )
    #except Alarm:
    #    #logger.error('command "%s", reached deadline try to terminate' % (command)) 
    #    # do not need time limit any more as the task have one 
    #    os.kill(p.pid, signal.SIGKILL)
    #    raise RuntimeError('command "%s", reached deadline and was terminated' % (command))
    if retcode != 0 :  # TO-DO need settings.FLAGS.RETRY.RETCODE
        #logger.warning('command "%s", exit: %d <br> %s' % (command, retcode, error))
        raise self.retry(exc = Exception("Exit at code:"  + str(retcode) + ";" + error.decode('utf-8') ) )
    #return (output.decode( decode ), error.decode( decode  ), retcode)
    return [  retcode ]

