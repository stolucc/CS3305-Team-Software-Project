import pygame, sys
from pygame.locals import *

pygame.init()

DISPLAYSURF = pygame.display.set_mode((0, 0))
#pygame.display.set_caption('Music')

pygame.mixer.music.load("bla.mp3") # replace this with whatever song we're using
pygame.mixer.music.play(-1)

while True: # Main Loop

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()