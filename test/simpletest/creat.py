#!/usr/bin/env python
import os
loopFrom = 0
loopNum =  100
setName =  True
NamePre = "test"
argStr  = " 1 2 3 "
outputPre = "out."
errorPre = "err."
outdir = "output"

for ii in range( loopNum ):
    i = loopFrom + ii
    name = NamePre + str(i) if setName else ""
    arg = argStr + str(i)  if ii > 0 else "e " + str(i)
    outfile = os.path.join( outdir , outputPre +  str(i) )
    errfile = os.path.join( outdir , errorPre +  str(i) )
    print( " %s  %s > %s 2> %s  "  % ( name , arg  , outfile , errfile )  )
