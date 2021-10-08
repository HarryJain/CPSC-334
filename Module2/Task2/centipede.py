# Module imports
import pygame
from pygame import display as pydisplay, time as pytime, event as pyevent, font as pyfont, draw as pydraw, key as pykey
import serial
import threading
import random
from sys import argv
from os import path, makedirs


# Global constants

# Window constants for size, the fraction of player movment, and the window itself
WIDTH, HEIGHT = 480, 640
BOTTOM_FRAC = 2 / 3
WIN = pydisplay.set_mode((WIDTH, HEIGHT))

# The frames per second of the game
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

# esp_vals constants, including the repitions for smoothing input
REP_COUNT = 4
JOY_X = 0
JOY_Y = 1
JOY_BUTTON = 2
BUTTON = 3
SWITCH = 4

# Initialize the font and set the title of the window
pyfont.init()
pydisplay.set_caption("Centipede")

# List for storing input values from esp32 with non-action default values
esp_vals = [2800, 2800, 1000, 1000, 1]


def read_esp():
    ''' Sets up communication
    '''
    global esp_vals

    # Attach to the serial port for either the Pi or the Mac
    #   depending on CLI arguments
    if len(argv) > 1 and argv[1] == '--pi':
        ser = serial.Serial('/dev/ttyUSB0', 115200, timeout = 1)
    else:
        ser = serial.Serial('/dev/tty.SLAB_USBtoUART', 115200, timeout = 1)
    ser.flush()

    # Initialize a list for storing repitions of the sensor values to average
    reps = []

    # Continually update the esp_vals list
    while True:
        if ser.in_waiting > 0:
            #
            vals = ser.readline().decode('utf-8').rstrip().split(', ')
            vals = [ int(val) for val in vals if val != '' and val.isdigit() ]
            
            # Only add the values to the reps list if it has all 5 sensor values
            if len(vals) == 5:
                reps.append(vals)

            # If reps has REP_COUNT input readings, average thema and set esp_vals to them
            if len(reps) == REP_COUNT:
                esp_vals = [ int(sum([ reps[j][i] for j in range(REP_COUNT) ]) / REP_COUNT) for i in range(5) ]
                reps = []
                #print(esp_vals)


def collide(obj1, obj2):
    ''' Takes in two rectangle objects and returns a boolean of whether they
            are colliding at the given time.
    '''
    return obj1.colliderect(obj2)


class Laser:
    ''' Represents the lasers shot from the player at the centipede or barriers,
            with control of its drawing, movement, and collisions.
    '''
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
    ''' Represents the circle obstacles to the player and centipede movement,
            controlling its drawing and collisions.
    '''
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
    ''' Represents the player centipede shooter, controlling its drawing,
        its shooting, and its movement (along with that of its lasers)
    '''
    # Constant to prevent spamming the button and shooting too many lasers
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
        # Create basic new x and y values from the velocity
        newx = self.x + direction[0] * self.vel
        newy = self.y + direction[1] * self.vel
        # Set basic limits without regard for obstacles
        limits = [0, WIDTH - self.size + 1, int(HEIGHT * BOTTOM_FRAC), HEIGHT - self.size + 1]
        # Modify the limits if any objects are hit so the player cannot move through them
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
        # Move according to the basic x and y values and the limits
        self.x = newx if newx in range(limits[0], limits[1]) else limits[0] + self.vel - 1 if newx < limits[0] else limits[1] - self.vel
        self.y = newy if newy in range(limits[2], limits[3]) else limits[2] + self.vel - 1 if newy < limits[2] else limits[3] - self.vel

    def shoot(self):
        if self.cooldown_counter == 0:
            laser = Laser(self.x + self.size / 2 - 2, self.y - 20, 4, 20)
            self.laserz.append(laser)
            self.cooldown_counter = 1

    def cooldown(self):
        # If the cooldown is done, reset for more shooting
        if self.cooldown_counter >= self.COOLDOWN:
            self.cooldown_counter = 0
        # If the player just shot, iterate the cooldown counter
        elif self.cooldown_counter > 0:
            self.cooldown_counter += 1

    def move_lasers(self, speed, segments, obstacles):
        # Store a list of the segments and obstacles hit by the lasers
        hit = {'segments': [], 'obstacles': []}

        # Cooldown while the laser moves
        self.cooldown()

        # Move each of the lasers and check for collisions
        for laser in self.laserz:
            laser.move(speed)
            if laser.off_screen():
                self.laserz.remove(laser)
            else:
                # Check for hitting centipede segments, and if they are hit, 
                #   increase score accordingly
                for segment in segments:
                    if laser.collision(segment):
                        hit['segments'].append(segment)
                        segments.remove(segment)
                        self.score += 10
                        if laser in self.laserz:
                            self.laserz.remove(laser)
                # Check for hitting centipede segments, and if they are hit,
                #   shrink the obstacles and increase score accordingly
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
        # Returns the hit objects for later processing
        return hit


class Centipede:
    ''' Represents a whole centipede, containing a list of segments
            that move in unison until broken up.
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
        for segment in self.segments:
            segment.draw(window)

    def move(self, obstacles, player):
        # Move all the child segments
        if self.segments:
            # Move the head of the centipede and set a barrier for the movement
            #   of the other segments if it hits a barrier so they all move
            #   together
            prevx, prevy = self.segments[0].x, self.segments[0].y
            self.segments[0].move(self.limits, obstacles)
            if prevy != self.segments[0].y and len(self.segments) > 1:
                self.limits[self.segments[1].vel < 0] = prevx
            # Move the rest of the segments according to what the head does
            for segment in self.segments[1:]:
                segment.move(self.limits, obstacles)
                # Signal a loss of life if the player hits any segment
                if collide(segment.rect, player.rect):
                    return 'lose life'
            # Reset the x-limits to the screen limits
            self.limits = [0, WIDTH + 1]


class Segment:
    ''' Represents a single segment of a centipede, controlling its own
            drawing and movment (based on passed limits)
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
        # Create the default new x position
        newx = self.x - self.vel
        # If the segment is still emerging from the border, move until it
        #   is in bounds
        if self.state == START:
            self.x = newx
            if self.x in range(limits[0], limits[1]):
                self.state = NORMAL
        # If the segment is within the limits, move normally
        else:
            # Check for collisions with obstacles
            collision = False
            for obstacle in obstacles:
                if collide(self.rect, obstacle.rect):
                    collision = True
                    break
            # If the new x position is within the limits and there was no
            #   collision, just move normally
            if newx in range(limits[0], limits[1]) and not collision:
                self.x = newx
            # If you have reached a boundary, move the y coordinate and reverse
            #   the x direction
            else:
                newy = self.y + 2 * self.size * self.ydir
                # Flip the y-direction if it is on the boundary
                if newy not in range(int(HEIGHT * BOTTOM_FRAC) if self.state == END else 0, HEIGHT - self.size + 1):
                    self.ydir *= -1
                    newy = self.y + 2 * self.size * self.ydir
                self.y = newy
                # Reverse the x direction
                self.vel *= -1
                # Signal to stay in the bottom player area if you've reached it
                if self.y > int(HEIGHT * BOTTOM_FRAC):
                    self.state = END


def game():
    ''' Run the main program loop to play the game, updating every 1/FPS of
            a second.
    '''
    # Variable to determine whether to quit to the main menu
    run = True

    # Font variables
    main_font = pyfont.SysFont("comicsans", 30)
    label_height = 0

    # Clock used to time the screen refreshes
    clock = pytime.Clock()

    # Keep count of the number of screenshots
    screenshot_count = 0

    # Player variables
    lives = 3
    psize = 16
    pvel = 5
    player = Player(WIDTH / 2 - psize / 2, HEIGHT - psize - 10, psize, pvel)

    # Centipede variables
    centipedes = []
    cvel = 3
    csize = 9
    # Prevents the drawing of the "green screen" at the start of the game
    initial = True

    # Laser variables
    lvel = 8

    # Obstacle variables
    obstacles = []
    orects = []
    ocount = random.randint(20, 30)

    # Create ocount new obstacles at random possitions at least 6 times the
    #   radius away from each other
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

    def redraw_window(color = WHITE):
        ''' Localized function to redraw the base window and labels
        '''
        # Set the background color to color (WHITE by default)
        WIN.fill(color)

        # Draw the labels for score and lives in the corners
        score_label = main_font.render(f"Score: {player.score}", 1, NAVY)
        lives_label = main_font.render(f"Lives: {lives}", 1, NAVY)
        WIN.blit(score_label, (10, 10))
        WIN.blit(lives_label, (WIDTH - lives_label.get_width() - 10, 10))

        # Draw the player
        player.draw(WIN)

        # Draw the centipedes (whole centipedes)
        for centipede in centipedes:
            centipede.draw(WIN)

        # Draw the obstacles
        for obstacle in obstacles:
            obstacle.draw(WIN)

        # Actually update the screen
        pydisplay.update()

        # Return the height of the score label to adjust the 
        return score_label.get_height()

    # Set the pause indicator to False by default
    pause = False

    # Main update functionthat runs every 1 / FPS
    while run:
        # Update the clock and redraw the window
        clock.tick(FPS)
        label_height = redraw_window()

        # Check for quit, pause, and screenshot events
        for event in pyevent.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    pause = not pause
            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.image.save(WIN, path.join("screenshots", f"screenshot{screenshot_count}.jpg"))
                screenshot_count += 1
        
        # Check for switch pause events
        if not ((len(argv) > 1 and argv[1] == "--keyboard") or (len(argv) > 2 and argv[2] == "--keyboard")):
            pause = esp_vals[SWITCH] == 0

        # Check for joystick screenshot events
        if esp_vals[JOY_BUTTON] == 0:
            pygame.image.save(WIN, path.join("screenshots", f"screenshot{screenshot_count}.jpg"))
            screenshot_count += 1

        # Main action block when the game is not paused
        if not pause:
            # If there are no centipedes, create a new one
            if len(centipedes) == 0:
                # If it is not the initial level or a life lost, flash a
                #   green background to symbolize beating a level
                if not initial:
                    redraw_window(GREEN)
                    pause = True
                    for i in range(FPS * 2):
                        clock.tick(FPS)
                        # Allow for screenshots during "new level"
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

            # Handle key presses and inputs  of all sorts
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

            # Move the centipedes and check for collisions
            for centipede in centipedes:
                # If the player hits a centipede, flash a black screen and
                #   restart a "new level"
                if centipede.move(obstacles, player) == "lose life":
                    lives -= 1
                    centipedes.remove(centipede)
                    redraw_window(BLACK)
                    pause = True
                    for i in range(FPS * 2):
                        clock.tick(FPS)
                        # Allow for screenshots during "lose life"
                        for event in pyevent.get():
                            if event.type == pygame.MOUSEBUTTONDOWN:
                                pygame.image.save(WIN, path.join("screenshots", f"screenshot{screenshot_count}.jpg"))
                                screenshot_count += 1
                        if esp_vals[JOY_BUTTON] == 0:
                            pygame.image.save(WIN, path.join("screenshots", f"screenshot{screenshot_count}.jpg"))
                            screenshot_count += 1
                    pause = False
                    # Restart the centipede
                    initial = True
                    # End the game if you are out of lives
                    if lives <= 0:
                        run = False

            # Move the player lasers and add obstacles/remove segments wherever
            #   they are hit
            for centipede in centipedes:
                hits = player.move_lasers(-lvel, centipede.segments, obstacles)
                if hits['segments']:
                    for hit in hits['segments']:
                        obstacles.append(Obstacle(hit.x, hit.y, csize))
                # Delete the centipede if it has no segments
                if not centipede.segments: 
                    centipedes.remove(centipede)


def main():
    ''' Start the program by connecting the ESP32 if desired and showing
            a basic menu screen, while also dealing with quitting the program
    '''
    # Set the title font
    title_font = pyfont.SysFont("comicsans", 40)
    
    # Controls whether the game is running or quit
    run = True

    # Start the separate thread for getting ESP32 values if desired
    if not ((len(argv) > 1 and argv[1] == "--keyboard") or (len(argv) > 2 and argv[2] == "--keyboard")):
        esp_thread = threading.Thread(target = read_esp, name = "esp")
        esp_thread.start()

    # Make a directory for storing the screenshots
    makedirs('screenshots', exist_ok=True)

    # Run the game until the user quits (from the menu)
    while run:
        # Draw a basic menu screen
        WIN.fill(WHITE)
        title_label = title_font.render("Press the button to begin...", 1, NAVY)
        WIN.blit(title_label, (WIDTH / 2 - title_label.get_width() / 2, HEIGHT / 2 - title_label.get_height() / 2))
        pydisplay.update()
        # Start the game on either a touchpad/mouse or button click
        #   and quit when the window is closed
        for event in pyevent.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                game()
        if esp_vals[BUTTON] == 0 or esp_vals[JOY_BUTTON] == 0:
            game()
    pygame.quit()


# Run the main function to start
if __name__ == "__main__":
   main()
