from gpiozero import Button
from signal import pause
from os import system
from math import sqrt
from sys import exit

button = Button(2)
switch = Button(3)

joy_x = Button(15)
joy_y = Button(14)
joy_button = Button(4)

SPEED = 1000
XLIMIT = 100
YLIMIT = 100

players = []
player_index = 0

x = []
y = []
realx = []
realy = []

colors = {'red': '\33[41m', 'yellow': '\33[43m', 'green': '\33[42m', 'end': '\33[0m'}

def calc_dist():
    return sqrt((realx[0] - realx[player_index]) ** 2 + (realy[0] - realy[player_index]) ** 2)

def call():
    print(f'{players[player_index]}: {realx[player_index]}, {realy[player_index]}')
    if player_index != 0:
        dist = calc_dist()
        if dist < 15:
            print(f'{players[player_index]} found {players[0]} and wins!!!')
            exit(0)
        dist_color = 'green' if dist < 50 else 'yellow' if dist < 300 else 'red' 
        print(players[player_index] + ': Marco!')
        print(players[0] + ': '  + colors[dist_color] + 'Polo!' + colors['end'])
        print(dist)

def switch_player():
    global player_index
    player_index = (player_index + 1) % len(players)
    system('clear')
    call()

def draw():
    global x, y, realx, realy
    
    if realx[player_index] < XLIMIT and joy_x.is_pressed:
        x[player_index] += 1
    elif realx[player_index] > 0 and not joy_x.is_pressed:
        x[player_index] -= 1
    
    if x[player_index] % SPEED == 0:
        realx[player_index] = x[player_index] / SPEED

    if realy[player_index] < YLIMIT and joy_y.is_pressed:
        y[player_index] += 1
    elif realy[player_index] > 0 and not joy_y.is_pressed:
        y[player_index] -= 1
    
    if y[player_index] % SPEED == 0:
        realy[player_index] = y[player_index] / SPEED
    
    print(f'{players[player_index]}: {realx[player_index]}, {realy[player_index]}')
 
def stop():
    system('clear')
    call() 

def main():
    while True:    
        player_count = input('How many people are playing (must be at least 2): ')
        if player_count.isdigit() and int(player_count) > 1:
            player_count = int(player_count)
            break

    for i in range(player_count):
        players.append(input(f'Player {i} Name: '))
        x.append(0)
        y.append(0)
        realx.append(0)
        realy.append(0)
        

    button.when_pressed = switch_player
    
    switch.when_released = stop

    while True:
        if switch.is_pressed and not joy_button.is_pressed:
            draw()

if __name__ == "__main__":
    main()
