from gpiozero import Button
from signal import pause

button = Button(2)

def press_button():
    print("Stop pushing my buttons!")
    #while button.is_pressed:
    #    print("pushing...")

button.when_pressed = press_button

pause()
