import serial
import modbus_tk.defines as cst
import modbus_tk.modbus_rtu as modbus_rtu
import time
from datetime import datetime
import struct 


import requests

token = "rHr9SwDdrlELjivrBytAcKyFKlo4o3Qw"
ur4 = 'http://blynk-cloud.com/'+token+'/update/V0?value='
ur5 = 'http://blynk-cloud.com/'+token+'/update/V1?value='
ur6 = 'http://blynk-cloud.com/'+token+'/update/V2?value='
ur7 = 'http://blynk-cloud.com/'+token+'/update/V3?value='
# http://blynk-cloud.com/auth_token/update/pin?value=value
# import pyrebase
# import redis
# from pyModbusTCP.client import ModbusClient

SERVER_HOST = "192.168.200.18"
SERVER_PORT = 502
address_currpack = 8448

blynkToken = "Z3IpYgan8qOuvPBJ9XGxa1i-nLcbA3th"
url = 'http://119.18.158.238:3579/'+blynkToken


def pushBlynk(virtualPin,data):
    blynkUrl = url+"/update/"+virtualPin+"?value="+str(data)

    # dataBlynk4 = ur4+str(dataMppt1[4])
    blynkPush = requests.get(blynkUrl)
    print(blynkPush)
    print(blynkUrl)


# c = ModbusClient()

# c.host(SERVER_HOST)
# c.port(SERVER_PORT)
# c.open()


master = modbus_rtu.RtuMaster(serial.Serial(
    "/dev/ttyS0", baudrate=9600, parity='N', stopbits=1, bytesize=8))
master.open
master.set_timeout(10)
master.set_verbose(True)

# def tes_mppt():
#     curr = c.read_holding_registers(58634, 16)
#     time.sleep(0.5)
#     return curr


def tes_mppt(uid):
    try:
        master = modbus_rtu.RtuMaster(serial.Serial(
            "/dev/ttyS0", baudrate=115200, parity='N', stopbits=1, bytesize=8))
        master.open
        master.set_timeout(10)
        master.set_verbose(True)
        read = master.execute(uid, cst.READ_INPUT_REGISTERS, 12544, 6)
        time.sleep(0.5)
        return read
    except:
        print("error")
   #     master.close()


def tes_chint(uid):
    try:
        master = modbus_rtu.RtuMaster(serial.Serial(
            "/dev/ttyS0", baudrate=9600, parity='N', stopbits=1, bytesize=8))
        master.open
        master.set_timeout(10)
        master.set_verbose(True)
        read = master.execute(uid, cst.READ_INPUT_REGISTERS, 8198, 6)

        shi2000 =  toFloat32(read[2],read[3])
        shi3000 =  toFloat32(read[4],read[5])
        pushBlynk("V41",shi3000)
        pushBlynk("V42",shi2000)

        time.sleep(0.5)
        return read
    except:
        print("error")
  #      master.close()

def tes_mppt_energy(uid):
    try:
        master = modbus_rtu.RtuMaster(serial.Serial(
            "/dev/ttyS0", baudrate=115200, parity='N', stopbits=1, bytesize=8))
        master.open
        master.set_timeout(10)
        master.set_verbose(True)
        read = master.execute(uid, cst.READ_INPUT_REGISTERS, 13068, 2)
        time.sleep(0.5)
        return float(read[0])/100
    except:
        print("error")

def toFloat32(val1,val2):
        nilai_a = val1
        nilai_b = val2
        hex_a = str()
        hex_b = str()
        if nilai_a == 0:
            hex_a = '0x0000'
        else:
            hex_a = hex(nilai_a)
        if nilai_b == 0:
            hex_b = '0x0000'
        else:
            hex_b = hex(nilai_b)
        str_ab = hex_a[2:] + hex_b[2:]
        if len(str_ab) % 2 != 0:
            str_ab += '0'
        bin_ab = bytes.fromhex(str_ab)
        FLOAT = 'f'
        fmt = '!' + FLOAT * (len(bin_ab) // struct.calcsize(FLOAT))

        num_ab = struct.unpack(fmt,bin_ab)[0]

        print(num_ab)

        return num_ab


def forSaveData(nama_file, data):
    log = open(nama_file, "a")
    log.write(data+'\n')
    log.close()


while True:
    now = datetime.now()
    dataJam = now.strftime("%Y-%m-%d %H:%M:%S")
    waktu = str(dataJam)
    # readDock(str(dataJam) + " ")
    dataChint = tes_chint(1)
    if dataChint != None:
        
        print("Chint :" + str(dataChint))
        forSaveData("/home/pi/ehubv3/loggerMacan/chint.txt",
                    str(waktu) + " Chint : " + str(dataChint))
    time.sleep(0.1)
    break
while True:
    dataMppt1 = tes_mppt(1)
    if dataMppt1 != None:
        print("MPPT 1 :" + str(dataMppt1))
        forSaveData("/home/pi/ehubv3/loggerMacan/mppt1.txt",
                    str(waktu) + " MPPT1 : " + str(dataMppt1))
        dataBlynk4 = ur4+str(dataMppt1[4])
        x4 = requests.get(dataBlynk4)
    time.sleep(0.1)
    break
while True:
    dataMppt2 = tes_mppt(2)
    if dataMppt2 != None:
        print("MPPT 2 :" + str(dataMppt2))
        forSaveData("/home/pi/ehubv3/loggerMacan/mppt2.txt",
                    str(waktu) + " MPPT2 : " + str(dataMppt2))
        dataBlynk4 = ur5+str(dataMppt2[4])
        x4 = requests.get(dataBlynk4)
    time.sleep(0.1)
    break
while True:
    dataMppt3 = tes_mppt(3)
    if dataMppt3 != None:
        print("MPPT 3 :" + str(dataMppt3))
        forSaveData("/home/pi/ehubv3/loggerMacan/mppt3.txt",
                    str(waktu) + " MPPT3 : " + str(dataMppt3))
        dataBlynk4 = ur6+str(dataMppt3[4])
        x4 = requests.get(dataBlynk4)
    time.sleep(0.1)
    break
while True:
    dataMppt4 = tes_mppt(4)
    if dataMppt4 != None:
        print("MPPT 4 :" + str(dataMppt4))
        forSaveData("/home/pi/ehubv3/loggerMacan/mppt4.txt",
                    str(waktu) + " MPPT4 : " + str(dataMppt2))
        dataBlynk4 = ur7+str(dataMppt4[4])
        x4 = requests.get(dataBlynk4)
        
    time.sleep(0.1)
    break

while True:
    dataMpptEnergy1 = tes_mppt_energy(1)
    if dataMpptEnergy1 != None:
        print ("energy 1 " + str(dataMpptEnergy1))
        virtual = "V53"
        pushBlynk(virtual,dataMpptEnergy1)
    time.sleep(0.1)
    break
while True:
    dataMpptEnergy1 = tes_mppt_energy(2)
    if dataMpptEnergy1 != None:
        print ("energy 2 " + str(dataMpptEnergy1))
        virtual = "V54"
        pushBlynk(virtual,dataMpptEnergy1)
    time.sleep(0.1)
    break

while True:
    dataMpptEnergy1 = tes_mppt_energy(3)
    if dataMpptEnergy1 != None:
        print ("energy 3 " + str(dataMpptEnergy1))
        virtual = "V55"
        pushBlynk(virtual,dataMpptEnergy1)
    time.sleep(0.1)
    break

while True:
    dataMpptEnergy1 = tes_mppt_energy(4)
    if dataMpptEnergy1 != None:
        print ("energy 4 " + str(dataMpptEnergy1))
        virtual = "V56"
        pushBlynk(virtual,dataMpptEnergy1)
    time.sleep(0.1)
    break
        


# while True:
#     dataMppt1 = tes_mppt(1)
#     if dataMppt1 != None:
#         print("MPPT 1 :" + str(dataMppt1))
#         break
#     time.sleep(1)

# while True:
#     dataMppt2 = tes_mppt(2)
#     if dataMppt2 != None:
#         print("MPPT 2 :" + str(dataMppt2))
#         break
#     time.sleep(1)

# while True:
#     dataChint = tes_chint(1)
#     if dataChint != None:
#         print("Chint :" + str(dataChint))
#         break
#     time.sleep(1)

# print(tes_mppt(2))
# curr = c.read_holding_registers(address_currpack, 16)
# print(curr)
