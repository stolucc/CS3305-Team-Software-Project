"""Module for menu to select object options."""
import pygame
import sys
from menu import Menu, MenuOption
from researchtree import ResearchTree


class TreeGUI(Menu):
    """Class for representing the visual of a tree."""

    def __init__(self, screen):
        self._screen = screen
        self._screen_width = self._screen.get_width()
        self._screen_height = self._screen.get_height()
        self._background_colour = (74, 74, 74)
        self._border = (63, 142, 252)
        self._text_colour = (0, 0, 0)
        self._text_size = 20

    def display_menu(self, tree):
        self.options = []
        self._start = []
        self._end = []
        option_width, option_height = 100, 40
        self.draw_background()
        branch = ""
        x_coordinate = 100
        y_coordinate = 50
        upgrade = 1
        print(tree.get_unlocked())
        for node in tree.get_unlocked():
            print(node)
            if node.branch != branch:
                y_coordinate += 100
                x_coordinate = 100
                branch = node.branch
            else:
                upgrade += 1
            option_block = pygame.Rect(
                x_coordinate, y_coordinate,
                option_width, option_height)
            self.draw_option(option_block, branch + str(upgrade))
            x_coordinate += 100
        pygame.display.flip()

    def draw_background(self):
        """Draw background for Tree."""
        block = pygame.Rect(
            (self._screen.get_width()-700)/2, 100,
            700, 500)
        pygame.draw.rect(self._screen, self._background_colour, block)
        pygame.draw.rect(self._screen, self._border, block, 3)

if __name__ == "__main__":
    screen = pygame.display.set_mode((1280, 720))
    pygame.font.init()

    def test():
        """Test Function."""
        print("test")

    tree = ResearchTree(None)
    menu = TreeGUI(screen)
    menu.display_menu(tree)
    while True:
        for event in pygame.event.get():   # User did something
            if event.type == pygame.QUIT:
                sys.exit()
