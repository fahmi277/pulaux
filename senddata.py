import can
from time import sleep


def main():
bus = can.interface.Bus(bustype='pcan', channel='PCAN_USBBUS1', bitrate=500000)

try:
    while True:

        # msg = can.Message(arbitration_id=0x232, data=[0x00], is_extended_id=False)
        # try:
        #     bus.send(msg)
        #     print("message sent on {}".format(bus.channel_info))
        # except can.CanError:
        #     print("message not sent!")

        msg = bus.recv(None)
        try:

            if msg.arbitration_id == 0x1B2:
                print(msg)

            if msg.arbitration_id == 0x1B3:
                print(msg)

            if msg.arbitration_id == 0x1B4:
                print(msg)

            if msg.arbitration_id == 0x1B5:
                print(msg)

        except AttributeError:
            print("Nothing received this time")

        sleep(0.2)

except KeyboardInterrupt:
    print("Program Exited")
except can.CanError:
    print("Message NOT sent")

bus.shutdown()


if __name__ == '__main__':
    main()
