import redis
from mppt.logger import logging, lvl_info

log = logging.getLogger()
log.setLevel(lvl_info)

PATH = '/home/pi/sundaya/dataLogging/'

red = redis.StrictRedis(
        host='localhost',
        port=6379,
        db=0,
        # password='9ff7b9d0-891b-4980-8559-6a67a76a73ac'
    )

def for_snmp(nama_file, data):
    log = open(nama_file, "w")
    log.write(data)
    log.close()

def redisWriteDataToSNMP(write=True):
    data = dict()
    for id in range(1,4):
        data[f'mppt{id}_pv_voltage'] = red.hget(f'mppt{id}', 'pv_voltage')
        data[f'mppt{id}_pv_current'] = red.hget(f'mppt{id}', 'pv_current')
        # data[f'mppt{id}_pv_power'] = red.hget(f'mppt{id}', 'pv_power')
    if write:
        for key, value in data.items():
            log.info(value)
            for_snmp(f'{PATH}{key}.txt', f'{float(data[key]) * 10}')

if __name__ == '__main__':
    redisWriteDataToSNMP(write=True)