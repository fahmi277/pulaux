#!/bin/bash
if [ "$1" = "-g" ]
then
echo .1.3.6.1.2.1.25.1.26 #lvd1
echo gauge
cat /home/pi/sundaya/dataLogging/canbus_voltage_max.txt
fi
exit 0
