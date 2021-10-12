# Module imports
import pygame
from pygame import display as pydisplay, time as pytime, event as pyevent, font as pyfont, draw as pydraw, key as pykey
import serial
import threading
import random
from sys import argv
from os import path


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
NAVY = (0, 41, 87)
GREEN = (161, 200, 169)
RED = (229, 69, 35)
YELLOW = (255, 213, 75)
BLUE = (42, 65, 158)
PINK = (253, 138, 153)
ORANGE = (241, 136, 11)
PURPLE = (165, 130, 210)

# Colors usable for the barriers
ocolors = [RED, YELLOW, BLUE, PINK, ORANGE, PURPLE]


# Arcade colors (defunct)
'''
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
'''

# Centipede state constants
START = 0
NORMAL = 1
END = 2

# esp_vals constants
REP_COUNT = 4
JOY_X = 0
JOY_Y = 1
JOY_BUTTON = 2
BUTTON = 3
SWITCH = 4


# Initialize the font and set the title of the window
pyfont.init()
pydisplay.set_caption("Centipede")


# Define list for storing input values from esp32
esp_vals = [2800, 2800, 1000, 1000, 1]


def read_esp():
    global esp_vals

    if len(argv) > 1 and argv[1] == '--pi':
        ser = serial.Serial('/dev/ttyUSB0', 115200, timeout = 1)
    else:
        ser = serial.Serial('/dev/tty.SLAB_USBtoUART', 115200, timeout = 1)
        ser.flush()

    reps = []

    while True:
        if ser.in_waiting > 0:
            vals = ser.readline().decode('utf-8').rstrip().split(', ')
            vals = [ int(val) for val in vals if val != '' and val.isdigit() ]
            if len(vals) == 5:
                reps.append(vals)
            if len(reps) == REP_COUNT:
                esp_vals = [ int(sum([ reps[j][i] for j in range(REP_COUNT) ]) / REP_COUNT) for i in range(5) ]
                reps = []
                #print(esp_vals)


def collide(obj1, obj2):
    return obj1.colliderect(obj2)


class Laser:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, window):
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pydraw.rect(window, BLACK, self.rect)

    def move(self, vel):
        self.y += vel

    def off_screen(self):
        return self.y < 0 or self.y > HEIGHT

    def collision(self, obj):
        return collide(self.rect, obj.rect)


class Obstacle:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius
        self.rect = pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)
        self.color = ocolors[random.randint(0, len(ocolors) - 1)]

    def draw(self, window):
        self.rect = pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)
        pydraw.circle(window, self.color, (self.x, self.y), self.radius, self.radius)

    def collision(self, obj):
        return collide(self.rect, obj.rect)


class Player:
    ''' Class to represent the player bug shooter
    '''
    COOLDOWN = 30

    def __init__(self, x, y, size, vel):
        self.x = x
        self.y = y
        self.size = size
        self.vel = vel
        self.laserz = []
        self.cooldown_counter = 0
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)
        self.score = 0

    def draw(self, window):
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)
        pydraw.rect(window, NAVY, self.rect)
        for laser in self.laserz:
            laser.draw(window)

    def move(self, direction, obstacles):
        newx = self.x + direction[0] * self.vel
        newy = self.y + direction[1] * self.vel
        limits = [0, WIDTH - self.size + 1, int(HEIGHT * BOTTOM_FRAC), HEIGHT - self.size + 1]
        for obstacle in obstacles:
            if collide(self.rect, obstacle.rect):
                if self.rect.x > obstacle.rect.x:
                    limits[0] = self.rect.x
                if self.rect.x < obstacle.rect.x:
                    limits[1] = self.rect.x
                if self.rect.y > obstacle.rect.y:
                    limits[2] = self.rect.y
                if self.rect.y < obstacle.rect.y:
                    limits[3] = self.rect.y
        self.x = newx if newx in range(limits[0], limits[1]) else limits[0] + self.vel - 1 if newx < limits[0] else limits[1] - self.vel
        self.y = newy if newy in range(limits[2], limits[3]) else limits[2] + self.vel - 1 if newy < limits[2] else limits[3] - self.vel

    def shoot(self):
        if self.cooldown_counter == 0:
            laser = Laser(self.x + self.size / 2 - 2, self.y - 20, 4, 20)
            self.laserz.append(laser)
            self.cooldown_counter = 1

    def cooldown(self):
        if self.cooldown_counter >= self.COOLDOWN:
            self.cooldown_counter = 0
        elif self.cooldown_counter > 0:
            self.cooldown_counter += 1

    def move_lasers(self, speed, segments, obstacles):
        hit = {'segments': [], 'obstacles': []}
        self.cooldown()
        for laser in self.laserz:
            laser.move(speed)
            if laser.off_screen():
                self.laserz.remove(laser)
            else:
                for segment in segments:
                    if laser.collision(segment):
                        hit['segments'].append(segment)
                        segments.remove(segment)
                        self.score += 10
                        if laser in self.laserz:
                            self.laserz.remove(laser)
                for obstacle in obstacles:
                    if laser.collision(obstacle):
                        hit['obstacles'].append(obstacle)
                        self.score += 1
                        obstacle.radius -= 3
                        obstacle.color = ocolors[random.randint(0, len(ocolors) - 1)]
                        if obstacle.radius <= 0:
                            obstacles.remove(obstacle)
                        if laser in self.laserz:
                            self.laserz.remove(laser)
        return hit


class Centipede:
    ''' Class to represent a whole centipede
    '''
    def __init__(self, x, y, radius, vel):
        self.x = x
        self.y = y
        self.radius = radius
        self.vel = vel
        self.ydir = 1
        self.state = START
        self.length = random.randint(10, 12)
        self.segments = [ Segment(WIDTH + i * self.radius * 2, self.y, self.radius, self.vel) for i in range(self.length) ]
        self.limits = [0, WIDTH + 1]

    def draw(self, window):
        # for i in range(self.length):
        #     self.segments[i].draw(window)
        for segment in self.segments:
            segment.draw(window)

    def move(self, obstacles, player):
        if self.segments:
            prevx, prevy = self.segments[0].x, self.segments[0].y
            self.segments[0].move(self.limits, obstacles)
            if prevy != self.segments[0].y and len(self.segments) > 1:
                self.limits[self.segments[1].vel < 0] = prevx

            # for i in range(1, self.length):     
            #     self.segments[i].move(self.limits)
            for segment in self.segments[1:]:
                segment.move(self.limits, obstacles)
                if collide(segment.rect, player.rect):
                    return 'lose life'

            self.limits = [0, WIDTH + 1]


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
        self.rect = pygame.Rect(self.x - self.size, self.y - self.size, self.size * 2, self.size * 2)

    def draw(self, window):
        self.rect = pygame.Rect(self.x - self.size, self.y - self.size, self.size * 2, self.size * 2) 
        pydraw.circle(window, GREEN, (self.x, self.y), self.size, self.size)

    def move(self, limits, obstacles):
        newx = self.x - self.vel
        if self.state == START:
            self.x = newx
            if self.x in range(limits[0], limits[1]):
                self.state = NORMAL
        else:
            collision = False
            for obstacle in obstacles:
                if collide(self.rect, obstacle.rect):
                    collision = True
                    break
            if newx in range(limits[0], limits[1]) and not collision:
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


def game():
    ''' Run the main program loop
    '''
    # Pi
    # ser = serial.Serial('/dev/ttyUSB0', 115200, timeout = 1)
    # Mac
    # ser = serial.Serial('/dev/tty.SLAB_USBtoUART', 115200, timeout = 1)
    # ser.flush()
    # esp_thread = threading.Thread(target = read_esp, name = "esp")
    # esp_thread.start()

    # Top-level variables
    run = True
    lost = False

    lives = 3

    main_font = pyfont.SysFont("comicsans", 30)

    clock = pytime.Clock()

    screenshot_count = 0

    psize = 16
    pvel = 5
    player = Player(WIDTH / 2 - psize / 2, HEIGHT - psize - 10, psize, pvel)

    centipedes = []
    clength = random.randint(10, 13)
    cvel = 3
    csize = 9
    initial = True

    lvel = 8

    obstacles = []
    orects = []
    ocount = random.randint(20, 30)
    for i in range(ocount):
        valid = False
        while not valid:
            valid = True
            ox = random.randint(csize * 2, WIDTH - csize * 2)
            oy = random.randint(csize * 2 + 20, HEIGHT - csize * 2)
            new_rect = pygame.Rect(ox - csize * 3, oy - csize * 3, csize * 6, csize * 6)
            for orect in orects:
                if collide(orect, new_rect):
                    valid = False
        obstacles.append(Obstacle(ox, oy, csize))
        orects.append(new_rect)

    label_height = 0

    # Localized function to redraw the base window and labels
    def redraw_window(color = WHITE):
        WIN.fill(color)

        score_label = main_font.render(f"Score: {player.score}", 1, NAVY)
        lives_label = main_font.render(f"Lives: {lives}", 1, NAVY)

        WIN.blit(score_label, (10, 10))
        WIN.blit(lives_label, (WIDTH - lives_label.get_width() - 10, 10))

        player.draw(WIN)

        for centipede in centipedes:
            centipede.draw(WIN)

        for obstacle in obstacles:
            obstacle.draw(WIN)

        pydisplay.update()

        return score_label.get_height()

    pause = False

    while run:
        '''if ser.in_waiting > 0:
            esp_vals = ser.readline().decode('utf-8').rstrip().split(', ')
            esp_vals = [ int(val) for val in esp_vals if val != '' and val.isdigit() ]
            if len(esp_vals) == 5:
                joy_x, joy_y, joy_button, button, switch = esp_vals
                #print(esp_vals)'''

        clock.tick(FPS)
        label_height = redraw_window()

        for event in pyevent.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    pause = not pause
            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.image.save(WIN, path.join("screenshots", f"screenshot{screenshot_count}.jpg"))
                screenshot_count += 1
        
        if not ((len(argv) > 1 and argv[1] == "--keyboard") or (len(argv) > 2 and argv[2] == "--keyboard")):
            pause = esp_vals[SWITCH] == 0
            
        if esp_vals[JOY_BUTTON] == 0:
            pygame.image.save(WIN, path.join("screenshots", f"screenshot{screenshot_count}.jpg"))
            screenshot_count += 1

        if not pause:
            # clock.tick(FPS)
            #label_height = redraw_window()

            if len(centipedes) == 0:# or len(centipedes[0].segments) == 0:
                if not initial:
                    redraw_window(GREEN)
                    pause = True
                    for i in range(FPS * 2):
                        clock.tick(FPS)
                        for event in pyevent.get():
                            if event.type == pygame.MOUSEBUTTONDOWN:
                                pygame.image.save(WIN, path.join("screenshots", f"screenshot{screenshot_count}.jpg"))
                                screenshot_count += 1
                        if esp_vals[JOY_BUTTON] == 0:
                            pygame.image.save(WIN, path.join("screenshots", f"screenshot{screenshot_count}.jpg"))
                            screenshot_count += 1
                else:
                    initial = False
                pause = False
                centipedes = [Centipede(WIDTH, csize + label_height + 10, csize, cvel)]
                # clength = random.randint(10, 13)
                # for i in range(clength):
                #     centipede = Segment(WIDTH + i * csize * 2, csize + label_height + 10, csize, cvel)
                #     centipedes.append(centipede)
            
            # for event in pyevent.get():
            #     if event.type == pygame.QUIT:
            #         run = False
            #     if event.type == pygame.KEYDOWN:
            #         if event.key == pygame.K_p:
            #             pause = True if pause == False else False
            #     if event.type == pygame.MOUSEBUTTONDOWN:
            #         pygame.image.save(WIN, "screenshot.jpg")

            keys = pykey.get_pressed()
            # Move left
            if keys[pygame.K_LEFT] or esp_vals[JOY_X] < 2600:
                player.move((-1, 0), obstacles)
            # Move right
            if keys[pygame.K_RIGHT] or esp_vals[JOY_X] > 3000:
                player.move((1, 0), obstacles)
            # Move up
            if keys[pygame.K_UP] or esp_vals[JOY_Y] < 2600:
                player.move((0, -1), obstacles)
            # Move down
            if keys[pygame.K_DOWN] or esp_vals[JOY_Y] > 3000:
                player.move((0, 1), obstacles)
            # Shoot on space press
            if keys[pygame.K_SPACE] or esp_vals[BUTTON] == 0:
                player.shoot()

            for centipede in centipedes:
                if centipede.move(obstacles, player) == 'lose life':
                    lives -= 1
                    centipedes.remove(centipede)
                    redraw_window(BLACK)
                    pause = True
                    for i in range(FPS * 2):
                        clock.tick(FPS)
                        for event in pyevent.get():
                            if event.type == pygame.MOUSEBUTTONDOWN:
                                pygame.image.save(WIN, path.join("screenshots", f"screenshot{screenshot_count}.jpg"))
                                screenshot_count += 1
                        if esp_vals[JOY_BUTTON] == 0:
                            pygame.image.save(WIN, path.join("screenshots", f"screenshot{screenshot_count}.jpg"))
                            screenshot_count += 1
                    pause = False
                    initial = True
                    if lives <= 0:
                        run = False

            for centipede in centipedes:
                hits = player.move_lasers(-lvel, centipede.segments, obstacles)
                if hits['segments']:
                    for hit in hits['segments']:
                        obstacles.append(Obstacle(hit.x, hit.y, csize))
                if not centipede.segments: 
                    centipedes.remove(centipede)
    
            #obstacle_hits = player.move_lasers(-lvel, obstacles, False)
        # else:
        #     for event in pyevent.get():
        #         if event.type == pygame.QUIT:
        #             run = False
        #         if event.type == pygame.KEYDOWN:
        #             if event.key == pygame.K_p:
        #                 pause = True if pause == False else False
        #         if event.type == pygame.MOUSEBUTTONDOWN:
        #             pygame.image.save(WIN, "screenshot.jpg")

def main():
    title_font = pyfont.SysFont("comicsans", 40)
    run = True

    if not ((len(argv) > 1 and argv[1] == "--keyboard") or (len(argv) > 2 and argv[2] == "--keyboard")):
        esp_thread = threading.Thread(target = read_esp, name = "esp")
        esp_thread.start()

    while run:
        WIN.fill(WHITE)
        title_label = title_font.render("Press the button to begin...", 1, NAVY)
        WIN.blit(title_label, (WIDTH / 2 - title_label.get_width() / 2, HEIGHT / 2 - title_label.get_height() / 2))
        pydisplay.update()
        for event in pyevent.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                game()
        if esp_vals[BUTTON] == 0 or esp_vals[JOY_BUTTON] == 0:
            game()
    pygame.quit()


if __name__ == "__main__":
   main()
