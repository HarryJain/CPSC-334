from gpiozero import Button
from signal import pause
from time import sleep

x = Button(15)
y = Button(14)

def left():
    print("Joystick left")

def right():
    print("Joystick right")

def up():
    print("Joystick up")

def down():
    print("Joystick down")

x.when_pressed = left
x.when_released = right

y.when_pressed = down
y.when_released = up

'''
while True:
    print(x.is_pressed)
    sleep(1)
'''

pause()
