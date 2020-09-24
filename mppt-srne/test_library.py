# from mppt import MPPTSRNE
import logging
from time import sleep
import asyncio
# from pymodbus.client.asynchronous.serial import (
#     AsyncModbusSerialClient as ModbusClient)
# from pymodbus.client.asynchronous import schedulers

logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.DEBUG)

# port = 'COM7'
# mppt_ids = [1,]

# async def main_event(client):
#     # data = dict()
#     id = 1
#     # for id in mppt_ids:
#     data = await client.getTemperature(id)
#     log.info(data)

# if __name__ == '__main__':
#     # loop, client = ModbusClient(schedulers.ASYNC_IO, port='COM7', baudrate=9600, method='rtu')
#     # mppt = MPPTSRNE(client=client.protocol)
#     mppt = MPPTSRNE(port=port)
#     mppt.loop.run_until_complete(main_event(mppt))
#     mppt.loop.close()

from mppt_sync import MPPTSRNE

port = "/dev/ttyS0"
mppt_ids = [1,2,3]

async def per_event(id,client):
    pv = client.getPVInfo(id)
    await asyncio.sleep(1)
    return pv

async def main():
    mppt = MPPTSRNE(port=port)
    res = await asyncio.gather([per_event(1,mppt),per_event(2,mppt),per_event(3,mppt),])
    return res

if __name__ == '__main__':
    res = asyncio.run(main())
    print(res)