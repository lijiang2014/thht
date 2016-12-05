from __future__ import absolute_import , unicode_literals
from ht_celery.celery import app
import os
from subprocess import PIPE, Popen
import signal

@app.task
def add(x,y):
    return x + y

@app.task
def mul(x,y):
    return x * y

@app.task 
def xsum(numbers):
    return sum(numbers)


@app.task(bind = True , default_retry_delay = 1 , track_started = True , max_retries = 3  )
def run_command( self , command, env=None, timeout=600 , decode ='utf-8' ):
    env_backup = os.environ.copy()
    #for i in os.environ.keys() :
    #        os.unsetenv( i )
    args = [ "bash" , "-c" , "-l" , command ]
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
    except Alarm:
        #logger.error('command "%s", reached deadline try to terminate' % (command)) 
        # do not need time limit any more as the task have one 
        os.kill(p.pid, signal.SIGKILL)
        raise RuntimeError('command "%s", reached deadline and was terminated' % (command))
    if retcode != 0 :  # TO-DO need settings.FLAGS.RETRY.RETCODE
        #logger.warning('command "%s", exit: %d <br> %s' % (command, retcode, error))
        raise self.retry(exc = Exception("Exit at code:" ,retcode) , countdown = 1  , max_retries = 3 )
        pass
    return (output.decode( decode ), error.decode( decode  ), retcode)

