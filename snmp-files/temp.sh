#!/bin/bash
if [ "$1" = "-g" ]
then
echo .1.3.6.1.2.1.25.1.8 #temp
echo gauge
cat /sys/class/thermal/thermal_zone0/temp
fi
exit 0
