#!/bin/bash
if [ "$1" = "-g" ]
then
echo .1.3.6.1.2.1.25.1.23 #lvd2
echo gauge
cat /home/pi/sundaya/dataLogging/canbus_vsat_current.txt
fi
exit 0
