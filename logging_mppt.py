import redis
from time import sleep
from mppt.mpptsrne.sync import MPPTSRNE
from mppt.logger import logging, lvl_info
from mppt.mpptsrne import address as addr

log = logging.getLogger()
log.setLevel(lvl_info)

number_mppt = 3

baudrate = 9600
port = '/dev/ttyS0'
mppt = MPPTSRNE(port=port, baudrate=baudrate)

red = redis.StrictRedis(
        host='localhost',
        port=6379,
        db=0,
        # password='9ff7b9d0-891b-4980-8559-6a67a76a73ac'
    )

def getAllSerialNumber(store=True):
    for id in range(1,number_mppt + 1):
        serial_num = mppt.getSerialNumber(id)
        log.info(f'mppt {id} : {serial_num}')
        if store:
            red.hset(f'mppt{id}', 'serial_number', serial_num)
        sleep(0.5)

def getAllPVInfo(store=True):
    for id in range(1, number_mppt + 1):
        pvinfo = mppt.getPVInfo(id)
        log.info(f'mppt {id} : {pvinfo}')
        if store:
            red.hset(f'mppt{id}', 'pv_voltage', pvinfo.get('pv_voltage').get('value'))
            red.hset(f'mppt{id}', 'pv_current', pvinfo.get('pv_current').get('value'))
            # red.hset(f'mppt{id}', 'pv_power', pvinfo.get('pv_power').get('value'))
        sleep(0.1)

def getAllEnergy(store=True):
    for id in range(1, number_mppt + 1):
        energy = mppt.getEnergyDay(id)
        log.info(f'mppt {id} : {energy}')
        if store:
            red.hset(f'mppt{id}', 'harvest_energy', energy.get('harvest_energy').get('value'))
            red.hset(f'mppt{id}', 'enjoy_energy', energy.get('enjoy_energy').get('value'))
        sleep(0.2)

def settingParameter(id, value):
    # values = [557,552,547,547,547,537,490,480,470,460]
    
    # values = [540,536,532,532,532,532,490,480,470,460]
    values = value
    val_param = [int(val/4) for val in values]
    val_param.insert(0, 12336)
    val_param.insert(1, 0)
    rr = mppt.setRegisters(id, addr.SETTING_PARAMETER[0], val_param)
    return rr

def initialize(store=True):
    getAllSerialNumber(store=store)
    for id in range(1,4):
        sys_param = mppt.getRegisters(id, (0xE003, 12))
        log.info(f'{sys_param.registers}')
        # log.info(f'{sys_param.encode()}')
        sleep(2)
    # for id in range(1,4):
    # set1 = [548,544,540,540,540,536,490,480,470,460]
    # set2 = [552,548,544,544,544,540,490,480,470,460]
    # set3 = [556,552,548,548,548,544,490,480,470,460]
    # print(settingParameter(1, set1))
    # sleep(2)
    # print(settingParameter(2, set2))
    # sleep(2)
    # print(settingParameter(3, set3))
    # sleep(2)

def mainFlow(loop=True, store=True):
    while loop:
        try:
            getAllPVInfo(store=store)
            getAllEnergy(store=store)
        except Exception as e:
            log.info('Failed to run program')
            log.info(e)
        sleep(1)
    getAllPVInfo(store=store)
    # getAllEnergy(store=False)

if __name__ == '__main__':
    initialize(store=False)
    mainFlow(loop=True)