#!/bin/bash
if [ "$1" = "-g" ]
then
echo .1.3.6.1.2.1.25.1.25 #lvd1
echo gauge
cat /home/pi/sundaya/dataLogging/canbus_voltage_min.txt
fi
exit 0
