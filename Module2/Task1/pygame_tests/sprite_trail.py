import pygame
import os
 
width, height = 1280, 960
screen = pygame.display.set_mode((width, height))
h_center = ((height / 2) - 16)
w_center = (width / 2)
 
 
class Arrow(pygame.sprite.Sprite):
    def __init__(self, speed):
        pygame.sprite.Sprite.__init__(self)
        self.speed = speed
        self.image = load_png('Arrow.png')
        self.rect = self.image.get_rect()
        self.x = width / 2
        self.delta = self.speed
 
#---Moves the arrow back and forth along the screen---
    def update(self):
        screen.blit(self.image, (self.x, h_center))
        self.x += self.delta
        if self.x > width - 64:
            self.delta = -self.speed
        elif self.x < 0:
            self.delta = +self.speed
 
 
class Boxes(pygame.sprite.Sprite):
    def __init__(self, size, color, location):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.color = color
        self.location = location
        self.image = pygame.Surface((size, 32))
        self.image.fill(color)
        self.rect = self.image.get_rect()
# ---Blits image on screen---
 
    def create(self):
        screen.blit(self.image, (self.location, h_center))
 
# ---Gets the image and its rectangle ---
 
 
def load_png(name):
    #fullname = os.path.join("assets", name)
    fullname = name
    image = pygame.image.load(fullname)
    if image.get_alpha is None:
            image = image.convert()
    else:
            image = image.convert_alpha()
    return image
 
 
def main():
#---Loading basics for a window---
    pygame.display.set_caption('')
    background = pygame.image.load('Background.png').convert()
    clock = pygame.time.Clock()
    fps = 60
#---Creating groups for sprites---
    all_sprites = pygame.sprite.Group()
    arrow_sprites = pygame.sprite.Group()
    block_sprites = pygame.sprite.Group()
#---Creating color codes for easier access---
    red = (240, 0, 0)
    white = (255, 255, 255)
    green = (0, 240, 0)
#---Usable Boxes and Arrows---
    b_red1 = Boxes(80, red, w_center)
    a1 = Arrow(7)
#---Adding usable Boxes and Arrows to sprite groups---
    all_sprites.add(b_red1)
    all_sprites.add(a1)
    arrow_sprites.add(a1)
    block_sprites.add(b_red1)
    screen.blit(background, (0, 0))
#---Main loop---
    running = True
    while running:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
        arrow_sprites.clear(screen, background)
        arrow_sprites.update()
        arrow_sprites.draw(screen)
        pygame.display.update()
 
if __name__ == '__main__':
    pygame.init()
    main()
