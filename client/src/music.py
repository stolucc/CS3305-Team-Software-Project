"""Module for playing music and adding songs to Pygame display screens."""
import pygame
import sys

# Note: Songs must have a pygame display in order to work.
# For the main menu, we could use the menu's display


class Music:
    """Play a song."""

    def __init__(self, song):
        """Create a song and start playing it."""
        pygame.mixer.music.load(song)
        self.play()

    def play(self):
        """Play the song indefinitely."""
        pygame.mixer.music.play(-1)

    def pause(self):
        """Pause the song temporarily."""
        pygame.mixer.music.pause()

    def stop(self):
        """Stop the song and go back to the start."""
        pygame.mixer.music.stop()

    def mute(self):
        """Mute the song."""
        pygame.mixer.music.set_volume(0)

    def unpause(self):
        """Unpause the song."""
        pygame.mixer.music.unpause()

    def unmute(self):
        """Unmute the song."""
        pygame.mixer.music.set_volume(1)


if __name__ == "__main__":
    pygame.init()
    pygame.display.set_mode((0, 0))
    pygame.display.set_caption('Music')
    music = Music("../resources/music/Egmont_Overture_Op_84.mp3")
    while True:   # Main Loop

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()
