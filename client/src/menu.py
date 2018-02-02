"""Menu elements."""

import pygame
import sys


class MenuOption:
    """A Class for a single menu option in a menu."""

    def __init__(self, name, menu_function):
        """
        Create a new menu option.

        :param name: the name displayed on the menu option
        :param menu_function: the function the menu implements
        """
        self._name = name
        self._menu_function = menu_function

    @property
    def name(self):
        """
        Property for name.

        :return: the name of the menu option
        """
        return self._name

    @property
    def menu_function(self):
        """
        Property for menu function.

        :return: the result of menu function
        """
        return self._menu_function


class Menu:
    """A class for the Menu."""

    def __init__(self, options):
        """
        Create a new Menu object.

        :param options: a list of tuples that have a name and a menu function
        """
        self._options = []
        for i in options:
            self._options += [MenuOption(i[0], i[1])]

    def size_of_option(self, width, height):
        """
        Calculate the size of the menu options.

        :param width: the width of the surface
        :param height: the height of the surface
        :return: the width of the menu option (option_width)
                and the height (option_height)
        """
        option_height = height/len(self._options)
        option_width = width/2
        return option_width, option_height

    def display_menu(self, screen, screen_width, screen_height):
        """
        Display the Menu.

        :param screen: display object to add menu too
        :param screen_width: width of the surface
        :param screen_height: height of the surface
        """
        option_width, option_height = self.size_of_option(screen_width,
                                                          screen_height)
        colour_red = (255, 0, 0)
        for i in range(len(self._options)):
            pygame.draw.rect(screen, colour_red, pygame.Rect(
                screen_width / 2 - option_width/2,
                i*option_height, option_width, option_height-10))


def test():
    """Test function."""
    print("lol")


if __name__ == "__main__":
    menu = Menu([("Resume", test), ("Options", test), ("Exit", test)])
    colour_black = (0, 0, 0)
    colour_white = (255, 255, 255)
    colour_green = (0, 255, 0)
    screen_width, screen_height = (1600, 1200)
    screen = pygame.display.set_mode((screen_width, screen_height),
                                     pygame.HWSURFACE |
                                     pygame.DOUBLEBUF |
                                     pygame.RESIZABLE)
    menu.display_menu(screen, screen_width, screen_height)
    done = False
    while not done:
        for event in pygame.event.get():  # User did something
            if event.type == pygame.QUIT:
                sys.exit()
