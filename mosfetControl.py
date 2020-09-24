import RPi.GPIO as GPIO
# from shiftr_74HC595.shiftr_74HC595 import ShiftRegister
from time import sleep
import time
import binascii
import os
import can

# ea for discharge mosfet
# eb for charge mosfer

def mosfetControl (dockInput,mosBlock,mosStatus):

    dock = (int(dockInput)-1)*256

    selectMessage = 0 #default pilihan mosfet adalah charge

    dataMosblock = 0xea 
    dataMosStatus = 0xba 

    if mosBlock == 'input':
        dataMosblock = 0xeb # MOSFET CHARGE
    elif mosBlock == 'output':
        dataMosblock = 0xea #MOSFET DISCHARGE
        selectMessage = 1

    if mosStatus == 'on':
        dataMosStatus = 0x0f
    elif mosStatus == 'off':
        dataMosStatus = 0xba

    print(dock+429982054)
   

    

    try:
        # can0 = can.interface.Bus(channel = 'can0', bustype = 'socketcan_ctypes')# socketcan_native

        id1 = 429982054 + dock
        id2 = 430046819 - dock
        id3 = 312738150 + dock
        id4 = 312802915 - dock

        print ("Data Mosfet : " + str(mosStatus))

        if mosStatus == 'on':

            msg1 = can.Message(arbitration_id=id1, data=[dataMosblock ,0x64 ,100-selectMessage ,0x64 ,0x64 ,0x64 ,0x63 ,0x64], extended_id=True)
            msg2 = can.Message(arbitration_id=id2, data=[dataMosblock ,0x64 ,0x64], extended_id=True)
            msg3 = can.Message(arbitration_id=id3, data=[dataMosblock,0x64,dataMosStatus,0x64,0x64,0x64], extended_id=True)
            msg4 = can.Message(arbitration_id=id4, data=[dataMosblock,0x64,0x64], extended_id=True)
           

            can0.send(msg1)
            print(msg1)
            time.sleep(0.2)
            can0.send(msg2)
            print(msg2)
            time.sleep(0.2)
            can0.send(msg3)
            print(msg3)
            time.sleep(0.2)
            can0.send(msg4)
            print(msg4)
            time.sleep(0.2)

        if mosStatus == 'off':

            msg1 = can.Message(arbitration_id=id1, data=[dataMosblock ,0x64 ,100-selectMessage ,0x64 ,0x64 ,0x64 ,0x63 ,0x64], extended_id=True)          
            msg3 = can.Message(arbitration_id=id3, data=[dataMosblock,0x64,dataMosStatus,0x64,0x64,0x64], extended_id=True)
            msg2 = can.Message(arbitration_id=id2, data=[dataMosblock ,0x64 ,0x64], extended_id=True)
            msg4 = can.Message(arbitration_id=id4, data=[dataMosblock,0x64,0x64], extended_id=True)
           

            can0.send(msg1)
            print(msg1)
            time.sleep(0.2)
            can0.send(msg3)
            print(msg3)
            time.sleep(0.2)
            can0.send(msg2)
            print(msg2)
            time.sleep(0.2)
            can0.send(msg4)
            print(msg4)
            time.sleep(0.2)



        # can0.send(msg5)
        # os.system('sudo ifconfig can0 down')
        print("terkirim")
    except:
        print("eror")
        os.system('sudo ifconfig can0 down')
        time.sleep(0.5)
        os.system('sudo ip link set can0 type can bitrate 250000')
        os.system('sudo ifconfig can0 up')
        return "0","0","0","0"

os.system('sudo ip link set can0 type can bitrate 250000')
os.system('sudo ifconfig can0 up')
can0 = can.interface.Bus(channel = 'can0', bustype = 'socketcan_ctypes')# socketcan_native


# msg1 = can.Message(arbitration_id=1, data=[1,2,3,4,5,6,7,8], extended_id=True)
# can0.send(msg1)

# mosfetControl('1','output','on')

passcode = input("Nomor dock [spasi] input/output on/off === > ")
# while True:
inputStr = passcode.split()

# if inputStr[]

# while True :

mosfetControl(inputStr[0],inputStr[1],inputStr[2])
time.sleep(2)
print("send")


# print(passcode[0:1])
# print(passcode[1:2])
# print(passcode[2:3])


