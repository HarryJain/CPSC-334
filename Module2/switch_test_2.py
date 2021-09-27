from gpiozero import Button
from signal import pause

switch = Button(3)

while True:
    print(switch.is_pressed)
