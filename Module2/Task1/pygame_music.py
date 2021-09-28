import pygame, time

pygame.mixer.pre_init(44100, 16, 2, 4096)
pygame.mixer.init()
pygame.mixer.music.load('/home/pi/LocalDevelopment/CPSC-334/Module2/Task1/beatles/taxman.wav')
pygame.mixer.music.play()
while pygame.mixer.music.get_busy() == True:
    continue
pygame.mixer.music.stop()
pygame.mixer.quit()

'''
pygame.mixer.pre_init(44100, 16, 2, 4096)
pygame.init()
sound = pygame.mixer.Sound('/home/pi/LocalDevelopment/CPSC-334/Module2/Task1/beatles/taxman.wav')
sound.play()
pygame.time.wait(1000)
'''
