import pygame
import sys
from pygame.locals import *

# Note: Songs must have a pygame display in order to work.
# For the main menu, we could use the menu's display


class Music:

    """Plays a song"""

    def __init__(self, song):
        """Creates a song and starts playing it"""
        pygame.mixer.music.load(song)
        self.play()

    def play(self):
        """Plays the song indefinitely"""
        pygame.mixer.music.play(-1)

    def pause(self):
        """Pauses the song temporarily"""
        pygame.mixer.music.pause()

    def stop(self):
        """Stops the song and goes back to the start"""
        pygame.mixer.music.stop()

    def mute(self):
        """Mutes the song"""
        pygame.mixer.music.set_volume(0)

    def unpause(self):
        """Unpauses the song"""
        pygame.mixer.music.unpause()

    def unmute(self):
        """Unmutes the song"""
        pygame.mixer.music.set_volume(1)


if __name__ == "__main__":
    pygame.init()
    pygame.display.set_mode((0, 0))
    pygame.display.set_caption('Music')
    music = Music("../resources/music/Egmont_Overture_Op_84.mp3")
    while True:   # Main Loop

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()
