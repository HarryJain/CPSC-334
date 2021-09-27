from gpiozero import *
from signal import pause
from time import sleep

x = SmoothedInputDevice(15)
y = SmoothedInputDevice(14)

while True:
    print(x.is_active)
    sleep(1)

pause()
