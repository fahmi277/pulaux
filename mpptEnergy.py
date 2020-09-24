import serial
import modbus_tk.defines as cst
import modbus_tk.modbus_rtu as modbus_rtu
import time
from datetime import datetime
import struct 


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

dataMppt1 = tes_mppt_energy(1)
if dataMppt1 != None:
    print("MPPT 1 :" + str(dataMppt1))