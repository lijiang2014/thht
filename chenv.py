#!/usr/bin/env python
import os 
os.putenv("AAA" , "AAA")
os.system("echo $AAA")
os.environ["AAA"]="AAA"

############
(output , error , retcode) = run_command('/bin/bash  -c  " ssh ln2 env "'   )

output  = output.splitlines()

In [33]: for eachLine in output :
    ...:     a = eachLine.split('=' , 1)
    ...:     if len(a) == 2 :
    ...:        os.putenv( a[0] , a[1] )

##############################

(output , error , retcode) = run_command('''bash -c ' python -c"import os;print (os.environ)"' '''   )


##############################

into json and read json 

(output , error , retcode) = run_command('''bash -c ' python -c"import os;import json;a= dict(os.environ);pri
    ...: nt( json.dumps(a) ) "' '''   )

json.loads(output)      

In [67]: for envname , envval in envjs.items() :
    ...:     os.putenv( envname , envval )
    ...:     
    ...:     

##############################

#arun_command('/bin/bash  -c  "env "'   )
(output , error , retcode) = run_command('/bin/bash  -c  "env "'   )
output  = output.splitlines()

for eachLine in output :
    ...:     a = eachLine.split('=' , 1)
    ...:     print(a)

for eachLine in output :
    ...:     a = eachLine.split('=' , 1)
    ...:     os.putenv( a[0] , a[1] )


