import asyncio
import can
import os
import binascii
from time import sleep
idMsgVoltageCurr = [124045411, 124045410, 124045409, 124045408, 124045407, 124045406, 124045405, 124045404, 124045403, 124045402, 124045401, 124045400, 124045399, 124045398, 124045397, 124045396]
idMsgMosfet = [123979875, 123979874, 123979873, 123979872, 123979871, 123979870, 123979869, 123979868, 123979867, 123979866, 123979865, 123979864, 123979863, 123979862, 123979861, 123979860]
id17VoltCurr = 124045395

idMsgCellBatch1 = [123914339, 123914338, 123914337, 123914336, 123914335, 123914334, 123914333, 123914332, 123914331, 123914330, 123914329, 123914328, 123914327, 123914326, 123914325, 123914324]

idMsgCellBatch2 = [123848803, 123848802, 123848801, 123848800, 123848799, 123848798, 123848797, 123848796, 123848795, 123848794, 123848793, 123848792, 123848791, 123848790, 123848789, 123848788]

idMsgCellBatch3 = [123783267, 123783266, 123783265, 123783264, 123783263, 123783262, 123783261, 123783260, 123783259, 123783258, 123783257, 123783256, 123783255, 123783254, 123783253, 123783252]

idMsgCellBatch4 = [123717731, 123717730, 123717729, 123717728, 123717727, 123717726, 123717725, 123717724, 123717723, 123717722, 123717721, 123717720, 123717719, 123717718, 123717717, 123717716]
def conVoltAmp(dataIn):
    byteVp1 = dataIn[4:6]
    byteVp2 = dataIn[6:8]
    byteAp1 = dataIn[8:10]
    byteAp2 = dataIn[10:12]

    outputData1 = int(f'0x{byteVp1}', 0)
    outputData2 = int(f'0x{byteVp2}', 0)

    outputData3 = int(f'0x{byteAp1}', 0)
    outputData4 = int(f'0x{byteAp2}', 0)

    factorv = 0
    if outputData1 <= 100:

        factorv = 0
    elif outputData1 > 100:
        factorv = 1

    outputDataVoltage = 25700 - (outputData1+((outputData2-factorv)*256))

    factora = 0
    if outputData3 <= 100:
        factora = 0
    elif outputData3 > 100:
        factora = 1

    outputDataCurrent = 25700 - (outputData3+((outputData4-factora)*256))

    return outputDataVoltage, outputDataCurrent

# os.system('sudo ip link set can0 type can bitrate 250000')
# os.system('sudo ifconfig can0 up')
async def listen_sensor_arus(msg):
    """Regular callback function. Can also be a coroutine."""
    if msg.arbitration_id == 490784999:
        print(f"{msg.data}\tini sensor_arus")
        await asyncio.sleep(0.5)

def handleVoltCurr(msg):
    if msg.arbitration_id in idMsgVoltageCurr:
        dock = idMsgVoltageCurr.index(msg.arbitration_id) + 1
        hex_msg = binascii.hexlify(msg.data)
        dataBattery = str(hex_msg.decode("utf-8"))
        convData = conVoltAmp(dataBattery)
        print(f'voltcurr:: dock: {dock} data: {convData}')
#        await asyncio.sleep(0.1)
        # red.hset('pack_volt', dock, convData[0])
        # red.hset('pack_curr', dock, convData[1])

def handleReadMosfetState(msg):
    mos_state_definition = {
        '53': {
            'cmos' : 'ON',
            'dmos' : 'OFF'
        },
        '42': {
            'cmos' : 'OFF',
            'dmos' : 'ON'
        },
        '31': {
            'cmos' : 'ON',
            'dmos' : 'ON'
        },
        '65': {
            'cmos' : 'OFF',
            'dmos' : 'OFF'
        },
    }
    if msg.arbitration_id in idMsgMosfet:
        dock = idMsgMosfet.index(msg.arbitration_id) + 1
        hex_msg = binascii.hexlify(msg.data)
        msg2data = str(hex_msg.decode("utf-8"))
        mosfetdata= mos_state_definition.get(msg2data[:2])
        temp_top = 100 - int(msg2data[6:8], 16)
        temp_mid = 100 - int(msg2data[8:10], 16)
        temp_bot = 100 - int(msg2data[10:12], 16)
        temp_cmos = 100 - int(msg2data[12:14], 16)
        temp_dmos = 100 - int(msg2data[14:16], 16)
        print(f'temp top:: dock: {dock} data: {temp_top}')
        print(f'temp mid:: dock: {dock} data: {temp_mid}')
        print(f'temp bot:: dock: {dock} data: {temp_bot}')
        print(f'temp cmos:: dock: {dock} data: {temp_cmos}')
        print(f'temp dmos:: dock: {dock} data: {temp_dmos}')
        print(f'mosfet state:: dock: {dock} data: {mosfetdata}')


def handleCellVBatch1(msg):
    if msg.arbitration_id in idMsgCellBatch1:
        dock = idMsgCellBatch1.index(msg.arbitration_id) + 1
        hex_msg = binascii.hexlify(msg.data)
        msg2data = str(hex_msg.decode("utf-8"))
        cell1_v = 25700 - (int(msg2data[:2],16) + (int(msg2data[2:4],16) * 256))
        cell2_v = 25700 - (int(msg2data[4:6],16) + (int(msg2data[6:8],16) * 256))
        cell3_v = 25700 - (int(msg2data[8:10],16) + (int(msg2data[10:12],16) * 256))
        cell4_v = 25700 - (int(msg2data[12:14],16) + (int(msg2data[14:16],16) * 256))
        print(f'cell1_voltage:: dock: {dock} data:{cell1_v}')
        print(f'cell2_voltage:: dock: {dock} data:{cell2_v}')
        print(f'cell3_voltage:: dock: {dock} data:{cell3_v}')
        print(f'cell4_voltage:: dock: {dock} data:{cell4_v}')

def handleCellVBatch2(msg):
    if msg.arbitration_id in idMsgCellBatch2:
        dock = idMsgCellBatch2.index(msg.arbitration_id) + 1
        hex_msg = binascii.hexlify(msg.data)
        msg2data = str(hex_msg.decode("utf-8"))
        cell5_v = 25700 - (int(msg2data[:2],16) + (int(msg2data[2:4],16) * 256))
        cell6_v = 25700 - (int(msg2data[4:6],16) + (int(msg2data[6:8],16) * 256))
        cell7_v = 25700 - (int(msg2data[8:10],16) + (int(msg2data[10:12],16) * 256))
        cell8_v = 25700 - (int(msg2data[12:14],16) + (int(msg2data[14:16],16) * 256))
        print(f'cell5_voltage:: dock: {dock} data:{cell5_v}')
        print(f'cell6_voltage:: dock: {dock} data:{cell6_v}')
        print(f'cell7_voltage:: dock: {dock} data:{cell7_v}')
        print(f'cell8_voltage:: dock: {dock} data:{cell8_v}')


def handleCellVBatch3(msg):
    if msg.arbitration_id in idMsgCellBatch3:
        dock = idMsgCellBatch3.index(msg.arbitration_id) + 1
        hex_msg = binascii.hexlify(msg.data)
        msg2data = str(hex_msg.decode("utf-8"))
        cell9_v = 25700 - (int(msg2data[:2],16) + (int(msg2data[2:4],16) * 256))
        cell10_v = 25700 - (int(msg2data[4:6],16) + (int(msg2data[6:8],16) * 256))
        cell11_v = 25700 - (int(msg2data[8:10],16) + (int(msg2data[10:12],16) * 256))
        cell12_v = 25700 - (int(msg2data[12:14],16) + (int(msg2data[14:16],16) * 256))
        print(f'cell9_voltage:: dock: {dock} data:{cell9_v}')
        print(f'cell10_voltage:: dock: {dock} data:{cell10_v}')
        print(f'cell11_voltage:: dock: {dock} data:{cell11_v}')
        print(f'cell12_voltage:: dock: {dock} data:{cell12_v}')


def handleCellVBatch4(msg):
    if msg.arbitration_id in idMsgCellBatch4:
        dock = idMsgCellBatch4.index(msg.arbitration_id) + 1
        hex_msg = binascii.hexlify(msg.data)
        msg2data = str(hex_msg.decode("utf-8"))
        cell13_v = 25700 - (int(msg2data[:2],16) + (int(msg2data[2:4],16) * 256))
        cell14_v = 25700 - (int(msg2data[4:6],16) + (int(msg2data[6:8],16) * 256))
        print(f'cell13_voltage:: dock: {dock} data:{cell13_v}')
        print(f'cell14_voltage:: dock: {dock} data:{cell14_v}')

async def listen_batre(msg):
    if msg.arbitration_id != 490784999:
        print(f"{msg.data}\tini battery")
        await asyncio.sleep(1)

async def main():
    can0 = can.Bus('can0', bustype='socketcan_ctypes', receive_own_messages=False)
    reader = can.AsyncBufferedReader()
    logger = can.Logger('logfile.asc')
    id17VoltCurr = 124045395

#    filters = []
 #   filters.append({'can_id': idMsgVoltageCurr[0], 'can_mask': 134217727, 'extended': False})
  #  can0.set_filters(filters)
    listeners = [
#        listen_batre,  # Callback function
        reader,         # AsyncBufferedReader() listener
        logger,          # Regular Listener object
        handleVoltCurr,
        handleReadMosfetState,
        handleCellVBatch1,
        handleCellVBatch2,
        handleCellVBatch3,
        handleCellVBatch4,
#        listen_sensor_arus
    ]
    # listeners1 = [
    #     ini_test,  # Callback function
    #     reader,         # AsyncBufferedReader() listener
    #     logger          # Regular Listener object
    # ]
    # Create Notifier with an explicit loop to use for scheduling of callbacks
    loop = asyncio.get_event_loop()
    # notifier1 = can.Notifier(can0, listeners1, loop=loop)
    notifier = can.Notifier(can0, listeners, loop=loop)
    # Start sending first message
    # can0.send(can.Message(arbitration_id=0))

    print('1 : Bouncing 10 messages...')
    for _ in range(16):
        # Wait for next message from AsyncBufferedReader
        msg = await reader.get_message()
       # print(f'ini can msg {msg}')

        # Delay response
        # await asyncio.sleep(0.1)
        # msg.arbitration_id += 1
        # can0.send(msg)
    # Wait for last message to arrive
    await reader.get_message()
    print('Done! 1')

    # Clean-up
    notifier.stop()
    # notifier1.stop()
    can0.shutdown()

async def main1():
    can0 = can.Bus('can0', bustype='socketcan_ctypes')
    reader = can.AsyncBufferedReader()
    logger = can.Logger('logfile.asc')

    listeners = [
         reader,         # AsyncBufferedReader() listener
         logger,          # Regular Listener object
    #     handleVoltCurr,
    #     handleReadMosfetState,
    #     handleCellVBatch1,
    #     handleCellVBatch2,
    #     handleCellVBatch3,
    #     # handleCellVBatch4,
     ]

    # Create Notifier with an explicit loop to use for scheduling of callbacks
    loop = asyncio.get_event_loop()
    notifier = can.Notifier(can0, listeners, loop=loop)
    i = 0
    n = 16
    a = []
    print('2 : Bouncing 10 messages...')
    while i < n:
        print(i)
        msg = await reader.get_message()
        if msg.arbitration_id in idMsgVoltageCurr:
            dock = idMsgVoltageCurr.index(msg.arbitration_id) + 1
            a.append(msg.arbitration_id)
            print(msg.arbitration_id)
          #  red.lset('pms_active', dock, 1)
            i += 1
    # Wait for last message to arrive
    await reader.get_message()
    print(a)
    print('Done! 2')

    # Clean-up
    notifier.stop()
    can0.shutdown()

# Get the default event loop
if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(main())
    # Run until main coroutine finishes
    loop.run_until_complete(main1())
    loop.close()
