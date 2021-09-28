from gpiozero import Button
from signal import pause

button = Button(2)
switch = Button(3)

joy_x = Button(15)
joy_y = Button(14)

SPEED = 500
XLIMIT = 1000
YLIMIT = 500

colors = ['red', 'green', 'blue']
color_index = 0

x = 0
y = 0
realx = 0
realy = 0

def press_button(i):
    global color_index
    color_index = (color_index + 1) % len(colors)

def draw():
    global x, y, realx, realy
    
    if realx < XLIMIT and joy_x.is_pressed:
        x += 1
    elif realx > 0 and not joy_x.is_pressed:
        x -= 1
    
    if x % SPEED == 0:
        realx = x / SPEED

    if realy < YLIMIT and joy_y.is_pressed:
        y += 1
    elif realy > 0 and not joy_y.is_pressed:
        y -= 1
    
    if y % SPEED == 0:
        realy = y / SPEED

    print(f'{colors[color_index]}: {realx}, {realy}')
 
def main():
    button.when_pressed = press_button
    while True:
        if switch.is_pressed:
            draw()

if __name__ == "__main__":
    main()
