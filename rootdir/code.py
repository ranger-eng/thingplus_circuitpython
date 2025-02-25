import time
import digitalio
import board

print("Hello World!")

led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT
while True:
    led.value = True
    time.sleep(1)
    led.value = False
    time.sleep(1)
