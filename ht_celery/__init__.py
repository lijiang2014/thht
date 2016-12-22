# initial redis connect for storing tasks state
import os
import redis

thht_port = int( os.getenv( "THHT_PORT", 6379  ) )
thht_host = os.getenv( "THHT_HOST", None  )
if not thht_host :
    raise Exception("Error: No THHT_HOST SET")
redis_instance = redis.Redis( host= thht_host , port = thht_port ) 