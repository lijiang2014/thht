import sys
from rdbtools import RdbParser, RdbCallback

class MyCallback(RdbCallback) :
    ''' Simple example to show how callback works. 
        See RdbCallback for all available callback methods.
        See JsonCallback for a concrete example
    ''' 
    def set(self, key, value, expiry):
        print('%s = %s' % (str(key), str(value)))

    def hset(self, key, field, value):
        print('%s.%s = %s' % (str(key), str(field), str(value)))

    def sadd(self, key, member):
        print('%s has {%s}' % (str(key), str(member)))

    def rpush(self, key, value) :
        print('%s has [%s]' % (str(key), str(value)))

    def zadd(self, key, score, member):
        print('%s has {%s : %s}' % (str(key), str(member), str(score)))

callback = MyCallback()
parser = RdbParser(callback)
import sys
from rdbtools import RdbParser, RdbCallback

class MyCallback(RdbCallback) :
    ''' Simple example to show how callback works. 
        See RdbCallback for all available callback methods.
        See JsonCallback for a concrete example
    ''' 
    def set(self, key, value, expiry):
        print('%s = %s' % (str(key), str(value)))

    def hset(self, key, field, value):
        print('%s.%s = %s' % (str(key), str(field), str(value)))

    def sadd(self, key, member):
        print('%s has {%s}' % (str(key), str(member)))

    def rpush(self, key, value) :
        print('%s has [%s]' % (str(key), str(value)))

    def zadd(self, key, score, member):
        print('%s has {%s : %s}' % (str(key), str(member), str(score)))

callback = MyCallback()
parser = RdbParser(callback)
parser.parse('./dump.rdb')
