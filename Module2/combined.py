from gpiozero import Button
from signal import pause

button = Button(2)
switch = Button(3)

joy_x = Button(15)
joy_y = Button(14)

limit = 1000

colors = ['red', 'green', 'blue']
color_index = 0

x = 0
y = 0

def press_button(i):
    global color_index
    color_index = (color_index + 1) % len(colors)

def draw():
    global x, y
    
    if x < limit and not joy_x.is_pressed:
        x += 1
    elif x > 0 and joy_x.is_pressed:
        x -= 1
    
    if y < limit and joy_y.is_pressed:
        y += 1
    elif y > 0 and not joy_y.is_pressed:
        y -= 1
    
    print(f'{colors[color_index]}: {x}, {y}')
 
def main():
    button.when_pressed = press_button
    while True:
        if switch.is_pressed:
            draw()

if __name__ == "__main__":
    main()
