#!/bin/bash
if [ "$1" = "-g" ]
then
echo .1.3.6.1.2.1.25.1.15 #batt1 voltage
echo gauge
cat /home/pi/sundaya/dataLogging/mppt1_batt_volt.txt
fi
exit 0
