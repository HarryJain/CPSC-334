# Library imports for physical interfacing, terminal clearing, and distance calculations
from gpiozero import Button
from os import system
from math import sqrt

# Physical connections via GPIO
button = Button(2)
switch = Button(3)
joy_x = Button(15)
joy_y = Button(14)
joy_button = Button(4)

# Constants that can be modified to change gameplay
SPEED = 1000
XLIMIT = 100
YLIMIT = 100
TURN_LIMIT = 5

# Variables storing data about the players and their current game state
players = []
player_index = 0
turn = 0
eot = False
won = False

# Lists containing the actual x and y positions of the players as well as those shown on screen
x = []
y = []
realx = []
realy = []

# A dictionary of colors for printing proximity
colors = {'red': '\33[41m', 'yellow': '\33[43m', 'green': '\33[42m', 'end': '\33[0m'}

# Calculate the distance of the current player from Marco.
def calc_dist():
    return sqrt((realx[0] - realx[player_index]) ** 2 + (realy[0] - realy[player_index]) ** 2)

# Print out the player information after a move
def call():
    global won
    print(f'Turn {turn}')
    print(f'{players[player_index]}: {int(realx[player_index])}, {int(realy[player_index])}')
    
    # Print a call to Marco and the resulting distance if it is not Marco's turn
    if player_index != 0:
        dist = calc_dist() 
        dist_color = 'green' if dist < 50 else 'yellow' if dist < 300 else 'red' 
        print(players[player_index] + ': Marco!')
        print(players[0] + ': '  + colors[dist_color] + 'Polo!' + colors['end'])
        print(f'{players[0]} is {colors[dist_color]}{dist}{colors["end"]} away.')
        if dist < 15:
            print(f'{players[player_index]} found {players[0]} and wins!!!')
            won = True
    if not won:
        print('\nFlip the switch to the on position again to further change your position. Press the button to change to the next player.')

# Clear the screen and switch the turn to the next player
def switch_player():
    global turn, eot, player_index
    if not switch.is_pressed:
        player_index = (player_index + 1) % len(players)
        system('clear')
        turn = 0
        eot = False
        call()

# Move the current player according to the joystick input and print their position, slowing them down by the SPEED constant and keeping them with the limit constants
def move():
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
    
    print(f'{players[player_index]}: {int(realx[player_index])}, {int(realy[player_index])}')

# Stop the current player's movement and iterate their turn
def stop():
    global turn
    if eot == False:
        system('clear')
        turn += 1
        call() 

# Give the players instructions and run the main logic
def main():
    global eot

    # Welcome the players
    print('Welcome to terminal Marco Polo by Harry Jain. Check README.md for detailed instructions and rules, and enjoy the game!\n')

    # Take input for the number of players, looping until an integer between 2 and 9, inclusive, is chosen 
    while True:    
        player_count = input('How many people are playing (must be at least 2 and at most 9): ')
        if player_count.isdigit() and int(player_count) > 1:
            player_count = int(player_count)
            break
    
    # Ask for the players' names, add them to the players array, and add 0 values for x, y, realx, and realy
    for i in range(player_count):
        players.append(input(f'Player {i + 1} Name: '))
        x.append(0)
        y.append(0)
        realx.append(0)
        realy.append(0)
        
    # Switch the player mode/state when the button is pressed
    button.when_pressed = switch_player
    
    # Stop taking joystick input when the swithc is off
    switch.when_released = stop

    print('\nFlip the switch on for the "Marco" to start the game.')
    
    # Whenever the swith is pressed and the joystick button in not down (a pause button effectively), move the player
    while True and not won:
        if switch.is_pressed and not joy_button.is_pressed:
            if turn >= TURN_LIMIT:
                if eot == False:
                    print(f'\nYou have used all {TURN_LIMIT} turns. Turn off the switch and press the button to change to the next player.')
                    eot = True
            else:
                move()

# Call the main function
if __name__ == "__main__":
    main()
