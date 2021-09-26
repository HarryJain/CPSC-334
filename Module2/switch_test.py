from gpiozero import Button
from signal import pause

button = Button(3)

def switch_on():
    print("Pull the lever Kronk!")

def switch_off():
    print("Wrong lever!!!")

button.when_pressed = switch_on
button.when_released = switch_off

pause()
