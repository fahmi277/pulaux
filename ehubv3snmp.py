import serial
import datetime
import modbus_tk.defines as cst
import modbus_tk.modbus_rtu as modbus_rtu
import os
import can
import time
import binascii
import json
from datetime import datetime


idPack = [124045411, 124045410, 124045409, 124045408, 124045407, 124045406, 124045405, 124045404, 124045403, 124045402, 124045401,
        124045400, 124045399, 124045398, 124045397, 124045396,124045395 , 124045394, 124045393, 124045392, 124045391, 124045390, 124045389, 124045388, 124045387]


idPack2 = []

for x in range(0,16):
    idPack2.append(((idPack[0]-65536)-x))


# for x in range(1,17):
#     idPack2.append((idPack[x-1])-(65536*x))


print(idPack2)


baseId = 124045412
dataDock = []
messagePack = []
dataVpack = []
dataIpack = []
dataAll = []

newId = []

pack10 = ""

messagePack2 = []


def addtoJson(dockNumber, voltage, current):
    exportJson = {
        "Dock "+str(dockNumber): {
            "voltage": str(voltage),
            "current": str(current)
        }
    }

    return exportJson


def for_snmp(nama_file, data):
    log = open(nama_file, "w")
    log.write(data)
    log.close()


def forSaveData(nama_file, data):
    log = open(nama_file, "a")
    log.write(data+'\n')
    log.close()
    # print("saved : " + str(data))


def conversion(dataIn):

    byteVp1 = dataIn[4:6]
    byteVp2 = dataIn[6:8]
    byteAp1 = dataIn[8:10]
    byteAp2 = dataIn[10:12]

    outputData1 = int("0x"+byteVp1, 0)
    outputData2 = int("0x"+byteVp2, 0)

    outputData3 = int("0x"+byteAp1, 0)
    outputData4 = int("0x"+byteAp2, 0)

    factorv = 0  # 0 untuk a_a1 <<<<< 100, 100 jika  a_a1 >>>> 100
    if outputData1 <= 100:
        factorv = 0
    elif outputData1 > 100:
        factorv = 1

    outputDataVoltage = 25700 - (outputData1+((outputData2-factorv)*256))

    factora = 0  # 0 untuk a_a1 <<<<< 100, 100 jika  a_a1 >>>> 100
    if outputData3 <= 100:
        factora = 0
    elif outputData3 > 100:
        factora = 1

    outputDataCurrent = 25700 - (outputData3+((outputData4-factora)*256))

    # if selectData == "V":
    # outputDataVoltage = outputDataVoltage/100
    # if selectData == "A":
    # outputDataCurrent = outputDataCurrent/100

    dataVpack.append(outputDataVoltage)
    dataIpack.append(outputDataCurrent)
    return outputDataVoltage, outputDataCurrent


def readDock(waktu):
    global pack10
    global messagePack2
    # dockdata = dockdata-1
    try:
        data = []
        msg = can0.recv(60)
        uid = msg.arbitration_id
        if uid != 490784999:

            if uid in idPack2:
                # data = uid-65536
                data = 124045412-(uid+65536)
                hex_msg = binascii.hexlify(msg.data)
                dataBattery = str(hex_msg.decode("utf-8"))
                messagePack2.append("dock : " + str(data) + " " + str(dataBattery))



            #print (uid)
            if uid in idPack:
                data = baseId-uid
                hex_msg = binascii.hexlify(msg.data)
                dataBattery = str(hex_msg.decode("utf-8"))


                if data not in dataDock:

                    newId.append(data)
                    dataDock.append(data)
                    conversion(dataBattery)
                    # print("Dock " + str(data) + " : " +
                    #       str(conversion(dataBattery)))
                    # print(str(dataBattery) + "\n")
                    messagePack.append(dataBattery)
                    dataBattery = ""

                    # print(f'Dock : {data}')

                    # os.system('sudo ifconfig can0 down')
                    # time.sleep(0.5)
                    # os.system('sudo ip link set can0 type can bitrate 250000')
                    # os.system('sudo ifconfig can0 up')
                # forSaveData("/home/pi/ehubv3/logger/logger.txt",str(waktu) + " Dock : " + str(data))

    except:
        print("error coiii ")
        os.system('sudo ifconfig can0 down')
        time.sleep(2)
        os.system('sudo ip link set can0 type can bitrate 250000')
        os.system('sudo ifconfig can0 up')
        return "0", "0"


def readEM():
    try:
        data = []
        msg = can0.recv(0.1)
        uid = msg.arbitration_id

        if uid == 490784999:
            hex_msg = binascii.hexlify(msg.data)
            str_msg = str(hex_msg)
            # print(str_msg)
            byteA1 = "0x" + str_msg[6:8]
            bytemA1 = "0x" + str_msg[8:10]
            byteA2 = "0x" + str_msg[10:12]
            bytemA2 = "0x" + str_msg[12:14]
            # print (byteA1)
            # print (bytemA1)
            # print (byteA2)
            # print (bytemA2)
            dataAmpere1 = int(byteA1, 0)
            datamAmpere1 = int(bytemA1, 0)/100

            dataAmpere2 = int(byteA2, 0)
            datamAmpere2 = int(bytemA2, 0)/100

            currentEM1 = dataAmpere1+datamAmpere1
            currentEM2 = dataAmpere2+datamAmpere2

            # print("\n===  ===\n")

            # print ("Load Vsat : "+str(currentEM1))
            # print ("Load BTS : "+str(currentEM2))

            # print("\n===  ===\n")

            return str(currentEM1*100), str(currentEM2*100)

    except:
        os.system('sudo ifconfig can0 down')
        time.sleep(0.5)
        os.system('sudo ip link set can0 type can bitrate 250000')
        os.system('sudo ifconfig can0 up')
        return "0", "0"


def readMos():
    try:
        data = []
        msg = can0.recv(0.1)
        uid = msg.arbitration_id

        # print (uid)

        if uid == 123979859:
            hex_msg = binascii.hexlify(msg.data)
            str_msg = str(hex_msg)
            print("mos: "+str_msg)

    except:
        os.system('sudo ifconfig can0 down')
        time.sleep(0.5)
        os.system('sudo ip link set can0 type can bitrate 250000')
        os.system('sudo ifconfig can0 up')
        return "0", "0"


def readV():
    try:
        data = []
        msg = can0.recv(0.1)
        uid = msg.arbitration_id

        # print (uid)

        # if uid == 123979859:
        #     hex_msg = binascii.hexlify(msg.data)
        #     str_msg = str(hex_msg)
        #     print("mos: "+str_msg)

        # can message pembuka isinya pack V dan current

        if uid == 124045411:

            hex_msg = binascii.hexlify(msg.data)
            str_msg = str(hex_msg)
            # print(str_msg)
            byteVp1 = "0x" + str_msg[6:8]
            byteVp2 = "0x" + str_msg[8:10]

            byteIp1 = "0x" + str_msg[10:12]
            byteIp2 = "0x" + str_msg[12:14]

            # print(byteVp1)
            # print(byteVp2)
            # print(byteIp1)
            # print(byteIp2)

            v_b1 = int(byteVp1, 0)
            v_b2 = int(byteVp2, 0)

            factorv = 0  # 0 untuk a_a1 <<<<< 100, 100 jika  a_a1 >>>> 100
            if v_b1 <= 100 and v_b1 > 0:
                factorv = 0
            elif v_b1 > 100:
                factorv = 1

            v_pack = 25700 - (v_b1+((v_b2-factorv)*256))

            # print(v_b2)

            a_a1 = int(byteIp1, 0)
            a_a2 = int(byteIp2, 0)
            # print(a_a1)
            # print(a_a2)
            factor = 0  # 0 untuk a_a1 <<<<< 100, 100 jika  a_a1 >>>> 100
            if a_a1 <= 100 and a_a1 > 0:
                factor = 0
            elif a_a1 > 100:
                factor = 1
            i_pack = 25700 - (a_a1+((a_a2-factor)*256))

            # if i_pack<0:
            i_pack = abs(i_pack)
            # else:
            #     i_pack = 0

            # print(v_pack/100)
            return str(v_pack), str(i_pack)
            # print(i_pack/10) #nilai positif menandakan pengecasan, negatif menandakan penggunaan

    except:
        os.system('sudo ifconfig can0 down')
        time.sleep(0.5)
        os.system('sudo ip link set can0 type can bitrate 250000')
        os.system('sudo ifconfig can0 up')
        return "0", "0"


print("=== Ehub V3 ===")
print("=== Setup CANbus ===")

os.system('sudo service snmpd restart')
os.system('sudo ip link set can0 type can bitrate 250000')
os.system('sudo ifconfig can0 up')

time.sleep(1)

can0 = can.interface.Bus(
    channel='can0', bustype='socketcan_ctypes')  # socketcan_native


# while True:
#     readMos()


while True:
    dataV = readV()
    if dataV != None:
        print(dataV)
        for_snmp("/home/pi/sundaya/dataLogging/canbus_voltage.txt", dataV[0])
        for_snmp("/home/pi/sundaya/dataLogging/canbus_current.txt", dataV[1])
        break


while True:
    dataI = readEM()
    if dataI != None:
        print(dataI)
        for_snmp(
            "/home/pi/sundaya/dataLogging/canbus_vsat_current.txt", dataI[0])
        for_snmp(
            "/home/pi/sundaya/dataLogging/canbus_bts_current.txt", dataI[1])
        break

for x in range(0, 1000):

    now = datetime.now()
    dataJam = now.strftime("%Y-%m-%d %H:%M:%S")
    readDock(str(dataJam) + " ")


for x in range(0, len(dataDock)):
    dataAll.append(addtoJson(str(x+1), str(dataVpack[x]), str(dataIpack[x])))

# dataDock.sort()

try:
    forSaveData("/home/pi/ehubv3/logger/loggerDock.txt",
                str(dataJam) + " Dock : " + str(dataDock))
except:
    forSaveData("/home/pi/ehubv3/logger/errorLoggerDock.txt",
                str(dataJam) + " Dock Error")


try:
    for_snmp("/home/pi/sundaya/dataLogging/canbus_voltage_max.txt",
             str(max(dataVpack)))
except:
    print("error saving snmp volt")


try:
    for_snmp("/home/pi/sundaya/dataLogging/canbus_voltage_min.txt",
             str(min(dataVpack)))
except:
    print("error saving snmp current")


try:
    forSaveData("/home/pi/ehubv3/logger/loggerAllData.json",
                str(dataJam) + ":" + str(dataAll))
except:
    forSaveData("/home/pi/ehubv3/logger/errorLoggerDock.txt",
                str(dataJam) + " Saving All data Error")


print(newId)
print(len(newId))
# print(dataDock)
print(dataVpack)
print(dataIpack)


# print("pack10 : "+str(pack10))

for x in range(0,16):
    # pass
    print(str(messagePack2[x]) + " " + str(newId[x]) + " " + str(dataVpack[x]))


# print(dataDock)
# print(max(dataVpack))
# print(min(dataVpack))
# print(max(dataIpack))
# print(min(dataIpack))


# print(dataAll)
