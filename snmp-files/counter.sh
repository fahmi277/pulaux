#!/bin/bash
if [ "$1" = "-g" ]
then
echo .1.3.6.1.2.1.25.1.9 #counter 
echo gauge
cat /home/pi/sundaya/dataLogging/counter.txt
fi
exit 0
