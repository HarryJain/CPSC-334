from gpiozero import Button
from signal import pause

button = Button(4)

def press_button():
    print("Stop pushing my buttons!")

button.when_pressed = press_button

pause()
