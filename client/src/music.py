import pygame, sys
from pygame.locals import *

class Music:

    def __init__(self, song):

        pygame.mixer.music.load(song)
        pygame.mixer.music.play(-1)

if __name__ == "__main__":
    pygame.init()
    DISPLAYSURF = pygame.display.set_mode((0, 0))
    pygame.display.set_caption('Music')
    music = Music("bla.mp3")
    while True: # Main Loop

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()