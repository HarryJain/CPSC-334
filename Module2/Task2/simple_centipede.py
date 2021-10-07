# Module imports
import time
import random
import pygame
from pygame import display as pydisplay, time as pytime, event as pyevent, font as pyfont, draw as pydraw, key as pykey
from pygame import *

# Global constants

# Set window size and store a reference to it
WIDTH, HEIGHT = 480, 640
BOTTOM_FRAC = 2 / 3
WIN = pydisplay.set_mode((WIDTH, HEIGHT))

# Set the frames per second
FPS = 60

# Color constants
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

START = 0
NORMAL = 1
END = 2

UP = 1
DOWN = -1

# Initialize the font and set the title of the window
pyfont.init()
pydisplay.set_caption("Centipede")


class Player:
    ''' Class to represent the player bug shooter
    '''
    def __init__(self, x, y, size, vel):
        self.x = x
        self.y = y
        self.size = size
        self.vel = vel
        self.laserz = []
        self.cooldown_counter = 0

    def draw(self, window):
        pydraw.rect(window, RED, (self.x, self.y, self.size, self.size))

    def move(self, direction):
        newx = self.x + direction[0] * self.vel
        newy = self.y + direction[1] * self.vel
        self.x = newx if newx in range(WIDTH - self.size + 1) else 0 if newx < 0 else WIDTH - self.size
        self.y = newy if newy in range(int(HEIGHT * BOTTOM_FRAC), HEIGHT - self.size + 1) else int(HEIGHT * BOTTOM_FRAC) if newy < int(HEIGHT * BOTTOM_FRAC) else HEIGHT - self.size


class Centipede:
    ''' Class to represent a whole centipede
    '''
    def __init__(self, x, y, size, vel):
        self.x = x
        self.y = y
        self.size = size
        self.vel = vel
        self.ydir = 1
        self.state = START

    def draw(self, window):
        pydraw.circle(window, GREEN, (self.x, self.y), self.size, self.size)

    def move(self):
        newx = self.x - self.vel
        if self.state == START:
            self.x = newx
            if self.x in range(WIDTH + 1):
                self.state = NORMAL
        else:
            if newx in range(WIDTH + 1):
                self.x = newx
            else: 
                newy = self.y + 2 * self.size * self.ydir
                if newy not in range(int(HEIGHT * BOTTOM_FRAC) if self.state == END else 0, HEIGHT - self.size + 1):
                    self.ydir *= -1
                    newy = self.y + 2 * self.size * self.ydir
                self.y = newy
                self.vel *= -1
                if self.y > int(HEIGHT * BOTTOM_FRAC):
                    self.state = END


class Segment:
    ''' Class to represent a segment of a centipede
    '''
    def __init__(self, x, y, size, vel):
        self.x = x
        self.y = y
        self.size = size
        self.vel = vel
        self.ydir = 1
        self.state = START

    def draw(self, window):
        pydraw.circle(window, GREEN, (self.x, self.y), self.size, self.size)

    def move(self):
        newx = self.x - self.vel
        if self.state == START:
            self.x = newx
            if self.x in range(WIDTH + 1):
                self.state = NORMAL
        else:
            if newx in range(WIDTH + 1):
                self.x = newx
            else: 
                newy = self.y + 2 * self.size * self.ydir
                if newy not in range(int(HEIGHT * BOTTOM_FRAC) if self.state == END else 0, HEIGHT - self.size + 1):
                    self.ydir *= -1
                    newy = self.y + 2 * self.size * self.ydir
                self.y = newy
                self.vel *= -1
                if self.y > int(HEIGHT * BOTTOM_FRAC):
                    self.state = END


def main():
    ''' Run the main program loop
    '''
    # Top-level variables
    run = True
    score = 0
    lives = 5

    main_font = pyfont.SysFont("comicsans", 30)

    clock = pytime.Clock()

    psize = 24
    pvel = 5
    player = Player(WIDTH / 2 - psize / 2, HEIGHT - psize - 10, psize, pvel)

    centipedes = []
    clength = random.randint(10, 13)
    cvel = 2
    csize = 10

    label_height = 0

    # Localized function to redraw the base window and labels
    def redraw_window():
        WIN.fill(WHITE)

        score_label = main_font.render(f"Score: {score}", 1, BLACK)
        lives_label = main_font.render(f"Lives: {lives}", 1, BLACK)

        WIN.blit(score_label, (10, 10))
        WIN.blit(lives_label, (WIDTH - lives_label.get_width() - 10, 10))

        player.draw(WIN)

        for centipede in centipedes:
            centipede.draw(WIN)

        pydisplay.update()

        return score_label.get_height()


    while run:
        clock.tick(FPS)
        label_height = redraw_window()

        if len(centipedes) == 0:
            clength = random.randint(10, 13)
            for i in range(clength):
                centipede = Segment(WIDTH + i * csize * 2, csize + label_height + 10, csize, cvel)
                centipedes.append(centipede)
        
        for event in pyevent.get():
            if event.type == pygame.QUIT:
                run = False

        keys = pykey.get_pressed()
        # Move left
        if keys[pygame.K_LEFT]:
            player.move((-1, 0))
        # Move right
        if keys[pygame.K_RIGHT]:
            player.move((1, 0))
        # Move up
        if keys[pygame.K_UP]:
            player.move((0, -1))
        # Move down
        if keys[pygame.K_DOWN]:
            player.move((0, 1))

        for centipede in centipedes:
            centipede.move()


if __name__ == "__main__":
   main()