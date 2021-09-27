from gpiozero import Button
from signal import pause
from time import sleep

x1 = Button(15)
x2 = Button(14)

def left():
    print("Joystick left")

def right():
    print("Joystick right")

'''
x1.when_pressed = left
x1.when_released = right

x2.when_pressed = right
x2.when_released = left
'''

while True:
    print(x1.is_pressed)
    print(x2.is_pressed)
    sleep(1)

pause()
