import pygame
import sys
from pygame.locals import *


class Menu_Option:
    """A Class for a single menu option in a menu"""

    def __init__(self, name, function):
        """
        Creates a new menu option

        :param name: The name displayed on the menu option
        :param function: The function the menu implements
        """
        self._name = name
        self._function = function

    @property
    def name(self):
        """
        property for name

        :return: Returns name
        """
        return name

    def function(self):
        """
        Implements function

        :return: Returns result of function
        """
        return self._function()


class Menu:
    """ A class for the Menu """
    def __init__(self, options):
        """
        Creates a new Menu

        :param options: A list of tuples that have a name and a function
        """
        self._options = []
        for i in options:
            self._options += [Menu_Option(i[0], i[1])]

    def size_of_option(self, width, height):
        """
        Calculates the size of the menu options

        :param width: The width of the surface
        :param height: The height of the surface
        :return: return the width of the menu option (option_width)
                and the height (option_height)
        """

        option_height = height/len(self._options)
        option_width = width/2
        return option_width, option_height

    def display_menu(self, screen, screen_width, screen_height):
        """
        Displays the Menu

        :param screen: Display object to add menu too
        :param screen_width: Width of the surface
        :param screen_height: Height of the surface
        """
        option_width, option_height = self.size_of_option(screen_width,
                                                    screen_height)
        colour_red = (255, 0, 0)
        for i in range(len(self._options)):
            pygame.draw.rect(screen, colour_red, pygame.Rect(
                screen_width / 2 - option_width/2,
                i*option_height, option_width, option_height-10))


def test():
    print("lol")


if __name__ == "__main__":
    menu = Menu([("Resume", test), ("Options", test), ("Exit", test)])
    colour_black = (0, 0, 0)
    colour_white = (255, 255, 255)
    colour_green = (0, 255, 0)
    screen_width, screen_height = (1600 , 1200)
    screen = pygame.display.set_mode((screen_width, screen_height),
                                    HWSURFACE| DOUBLEBUF| RESIZABLE)
    menu.display_menu(screen, screen_width, screen_height)
    done = False
    while not done:
        for event in pygame.event.get(): # User did something
            if event.type == pygame.QUIT:
                sys.exit()
