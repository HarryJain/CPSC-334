import pygame

#pygame.mixer.pre_init(22050, -16, 2, 1024)
pygame.mixer.pre_init(48000, -16, 2, 4096)
#pygame.mixer.init(22050, -16, 2, 1024)

pygame.mixer.init()
pygame.mixer.music.load('eleanor.wav')
pygame.mixer.music.play()

#pygame.mixer.Channel(0).play(pygame.mixer.Sound('eleanor.wav'), -1)

while True:
    continue
