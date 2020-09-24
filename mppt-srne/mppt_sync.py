import logging
from pymodbus.client.sync import ModbusSerialClient as ModbusClient
from address import *


logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.DEBUG)

class MPPTSRNE:

    def __init__(self, port:str, baudrate:int=9600):
        self.__port = port
        self.__baudrate = baudrate
        self.client = ModbusClient(port=port, baudrate=baudrate, method='rtu',timeout=0.1)

    @property
    def port(self) -> str:
        return self.__port

    @property
    def baudrate(self) -> int:
        return self.__baudrate

    def setRegisters(self, id:int, addr:int, val:list):
        request = self.client.write_registers(addr, val, unit=id)
        return request.function_code

    def getRegisters(self, id:int, info:tuple) -> list:
        addr = info[0]
        length = info[1]
        # rr = self.client.read_holding_registers(addr, length, unit=id)
        response_register = self.client.read_holding_registers(addr, length, unit=id)
        # log.debug(rr.encode())
        return response_register

    def getPVInfo(self, id:int) -> dict:
        response = self.getRegisters(id, PV_INFO)
        response_dec = response.registers
        log.debug(response_dec)
        return {
            'pv_voltage': {
                'value':round(response_dec[0] * 0.1, 2),
                'satuan': 'Volt'
            },
            'pv_current': {
                'value': round(response_dec[1] * 0.01, 2),
                'satuan': 'Ampere'
            },
            'pv_power': {
                'value':round(response_dec[2], 2),
                'satuan': 'Joule/s or Watt'
            }
        }

    def getProductModel(self, id:int) -> list:
        response = self.getRegisters(id, PRODUCT_MODEL)
        response_bits = bytes.fromhex(response.encode().hex()[2:]).decode('utf-8').replace(" ","")
        log.debug(response_bits)
        return response_bits

    def getSoftwareVersion(self, id:int) -> str:
        response = self.getRegisters(id, SOFTWARE_VERSION)
        response_hex = response.encode().hex()[4:]
        process = [response_hex[i:i+2] for i in range(0, len(response_hex), 2)]
        software_ver = '.'.join(process)
        return software_ver

    def getHardwareVersion(self, id:int) -> str:
        response = self.getRegisters(id, HARDWARE_VERSION)
        response_hex = response.encode().hex()[4:]
        process = [response_hex[i:i+2] for i in range(0, len(response_hex), 2)]
        hardware_ver = ".".join(process)
        return hardware_ver

    def getSerialNumber(self, id:int) -> str:
        response = self.getRegisters(id,SERIAL_NUMBER)
        response_hex = response.encode().hex()[2:]
        return response_hex

    def getEnergyDay(self, id:int) -> dict:
        response = self.getRegisters(id, ENERGY_DAY)
        response_dec = response.registers
        log.debug(response)
        return {
            'harvest_energy': {
                'value': response_dec[0],
                'satuan': 'Joule/s or Watt'
            },
            'enjoy_energy': {
                'value': response_dec[1],
                'satuan': 'Joule/s or Watt'
            }
        }

    def getTemperature(self, id:int) -> dict:
        response = self.getRegisters(id, TEMPERATURE)
        response_hex = response.encode().hex()[2:]
        log.info(response_hex)
        return {
            'mppt_temp': {
                'value':int(response_hex[:2], base=16),
                'satuan': 'Celcius'
            },
            'batt_temp': {
                'value': int(response_hex[2:], base=16),
                'satuan': 'Celcius'
            }
        }


port = 'COM7'
mppt_ids = [1,]

def main_event(client):
    # data = dict()
    id = 1
    # for id in mppt_ids:
    data = client.getTemperature(id)
    log.info(data)

if __name__ == '__main__':
    # loop, client = ModbusClient(schedulers.ASYNC_IO, port='COM7', baudrate=9600, method='rtu')
    # mppt = MPPTSRNE(client=client.protocol)
    mppt = MPPTSRNE(port=port)
    mppt.loop.run_until_complete(main_event(mppt))
    mppt.loop.close()
