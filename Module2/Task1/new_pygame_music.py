import pygame

pygame.mixer.pre_init(22050, -16, 2, 1024)
pygame.init()
pygame.mixer.quit()
pygame.mixer.init(22050, -16, 2, 1024)

pygame.init()

pygame.mixer.Channel(0).play(pygame.mixer.Sound('taxman.wav'), -1)

while True:
    continue
