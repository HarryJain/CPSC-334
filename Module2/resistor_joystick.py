from gpiozero import Button
from signal import pause
from time import sleep

x1 = Button(17)
y1 = Button(4)

x2 = Button(15)
y2 = Button(14)

def left():
    print("Joystick left")

def right():
    print("Joystick right")

def up():
    print("Joystick up")

def down():
    print("Joystick down")

x1.when_pressed = right
x1.when_released = left

y1.when_pressed = up
y1.when_released = down

x2.when_pressed = left
x2.when_released = right

y2.when_pressed = down
y2.when_released = up

'''
while True:
    print(x.is_pressed)
    sleep(1)
'''

pause()
