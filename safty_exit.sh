#!/bin/sh

last_pro=`ps aux |  awk '$11=="'$THHT_EXEC_C'"{print $2 }' | wc -c` 
echo $last_pro
while [ $last_pro  -gt 0 ]
do
sleep 5
last_pro=`ps aux |  awk '$11=="'$THHT_EXEC_C'"{print $2 }' | wc -c`

done

