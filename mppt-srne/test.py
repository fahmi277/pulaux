import logging
# import asyncio
# from pymodbus.client.asynchronous.serial import (
#     AsyncModbusSerialClient as ModbusClient)
# from pymodbus.client.asynchronous import schedulers

logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.DEBUG)

# unit = 0x01

# async def read_address_modbus(client):
#     log.debug("Read address....")
#     # log.debug(rw.registers)
#     # rw = await client.write_register(26, 5, unit=unit)
#     rr = await client.read_holding_registers(263, 3, unit=unit)
#     log.debug(rr.registers)

# if __name__ == '__main__':
#     loop, client = ModbusClient(schedulers.ASYNC_IO, port='COM7', baudrate=9600, method='rtu')
#     loop.run_until_complete(read_address_modbus(client.protocol))
#     loop.close()


import modbus_tk.defines as cst
import modbus_tk.modbus_rtu as modbus_rtu
import serial


master = modbus_rtu.RtuMaster(serial.Serial("/dev/ttyS0", baudrate= 9600, parity='N', stopbits=1))
master.open
master.set_timeout(1)
master.set_verbose(True)



# read = master.execute(1, cst.WRITE_MULTIPLE_REGISTERS, 26 , output_value = [2])
read = master.execute(3,cst.READ_HOLDING_REGISTERS,0xE003, 1)
print(read)