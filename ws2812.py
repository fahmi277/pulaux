# Simple test for NeoPixels on Raspberry Pi

import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BCM) # Use physical pin numbering
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

import time
import board
import neopixel


# Choose an open pin connected to the Data In of the NeoPixel strip, i.e. board.D18
# NeoPixels must be connected to D10, D12, D18 or D21 to work.
pixel_pin = board.D18


num_pixels = 16

# The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
# For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
ORDER = neopixel.GRB

pixels = neopixel.NeoPixel(
    pixel_pin, num_pixels, brightness=0.2, auto_write=False, pixel_order=ORDER
)




    # Comment this line out if you have RGBW/GRBW NeoPixels

def controlLed(dock):
    dock = dock-1
    pixels[dock] = (0, 255, 0)
    pixels.show()

pixels.fill((255, 0, 0))
pixels.show()

while True: # Run forever
    if GPIO.input(23) == GPIO.HIGH:
        pixels.fill((0, 255, 0))
        pixels.show()
        time.sleep(5)
        pixels.fill((0, 0, 0))
        pixels.show()
        
#         pixels.fill((0, 0, 0))
#         pixels.show()
#         time.sleep(1)
        
        # break

#controlLed(15)
# while True:
#     pixels.fill((0, 255, 0))
#     pixels.show()
#     time.sleep(1)

