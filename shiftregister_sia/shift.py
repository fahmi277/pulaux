import RPi.GPIO as GPIO
from time import sleep
GPIO.setmode(GPIO.BCM)

ALL = -1
HIGH = 1
LOW = 0

class ShiftRegister:

    number_of_registers = 6
    SER_pin = 4
    RCLK_pin = 27
    SRCLK_pin = 17
    _register = list()

    def __init__(self,*args, **kwargs):
        # self._custompins = 0
        # if len(kwargs) > 0:
        #     self._custompins = 1
        self.ser_pin = kwargs.get('ser_pin', self.SER_pin)
        self.clk_pin = kwargs.get('clk_pin', self.RCLK_pin)
        self.srclk_pin = kwargs.get('srclk_pin', self.SRCLK_pin)
        self.num_of_registers = kwargs.get('num_of_registers', self.number_of_registers)

        # if self._custompins:
        #     if self.SER_pin != self.ser_pin or self.RCLK_pin != self.clk_pin or self.SRCLK_pin != self.srclk_pin:
        #         GPIO.setwarnings(True)
        # else:
        #     GPIO.setwarnings(False)

        GPIO.setup(self.ser_pin, GPIO.OUT)
        GPIO.setup(self.clk_pin, GPIO.OUT)
        GPIO.setup(self.srclk_pin, GPIO.OUT)
        self.num_of_pin_shiftregister = self.num_of_registers * 8

    def setOutput(self,pin, mode):
        '''
        Allows the user to set the state of a pin on the shift register
        '''
        if pin == ALL:
            self._all(mode)
        else:
            if len(self._register) == 0:
                self._all(LOW)

            self._setPin(pin, mode)

    def _all(self,mode, execute = True):
        self._all_shr = self.num_of_pin_shiftregister

        for pin in range(0, self._all_shr):
            self._setPin(pin, mode)
        if execute:
            self.latch()

        return self._register

    def _setPin(self,pin, mode):
        try:
            self._register[pin] = mode
        except IndexError:
            self._register.insert(pin, mode)

    def latch(self):
        all_pins = self.num_of_pin_shiftregister
        GPIO.output(self.clk_pin, GPIO.LOW)
        # print(self._register)
        for pin in range(all_pins -1, -1, -1):
            GPIO.output(self.srclk_pin, GPIO.LOW)

            pin_mode = self._register[pin]

            GPIO.output(self.ser_pin, pin_mode)
            GPIO.output(self.srclk_pin, GPIO.HIGH)

        GPIO.output(self.clk_pin, GPIO.HIGH)

    def cleanup(self):
        self._registers = []
        self.latch()

# obj = ShiftRegister(num_of_registers = 1)
# while True:
#     obj.digitalWrite(5, obj.HIGH)
#     sleep(1)
#     obj.digitalWrite(5, obj.LOW)
#     obj.cleanup()
#     sleep(1)
