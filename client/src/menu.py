import pygame
import sys
from pygame.locals import *


class MenuOption:
    """A Class for a single menu option in a menu"""

    def __init__(self, name, menu_function):
        """
        Create a new menu option.

        :param name: The name displayed on the menu option
        :param function: The function the menu implements
        """
        self._name = name
        self._menu_function = menu_function

    @property
    def name(self):
        """
        Property for name.

        :return: name
        """
        return self._name

    @property
    def menu_function(self):
        """
        Implement menu function.

        :return: result of menu_function
        """
        return self._menu_function()


class Menu:
    """A class for the Menu."""

    def __init__(self, screen, options):
        """
        Create a new Menu.

        :param options: A list of tuples that have a name and a function
        """
        self._options = []
        self._screen = screen
        for i in options:
            self._options += [MenuOption(i[0], i[1])]

    def set_screen(self, screen):
        self._screen = screen
    def text_objects(self, text, font, colour):
        """
        Create a text object.

        :param text: text that object will hold
        :param font: a pygame.font object
        :param colour: the colour of the text
        :return: a text object
        """
        textSurface = font.render(str(text), True, colour)
        return textSurface, textSurface.get_rect()

    def message_display(self, text, text_size, y_cord, x_cord, colour):
        """
        Display message on screen.

        :param screen: display object
        :param text: the text that will be display
        :param text_size: the size of the text in pixels
        :param y_cord: the y coordinate of the message
        :param x_cord: the x coordinate of the message
        :param colour: the colour the text will be
        """
        largeText = pygame.font.Font('freesansbold.ttf', text_size)
        TextSurf, TextRect = self.text_objects(text, largeText, colour)
        TextRect.center = (y_cord, x_cord + text_size/2)
        self._screen.blit(TextSurf, TextRect)

    def size_of_option(self, width, height):
        """
        Calculate the size of the menu options.

        :param width: The width of the surface
        :param height: The height of the surface
        :return: return the width of the menu option (option_width)
                and the height (option_height)
        """
        option_height_space = 20
        option_height = 35
        option_width = width/4
        return option_width, option_height, option_height_space

    def display_menu(self):
        """Display the menu."""
        pygame.font.init()
        colour_black = (0, 0, 0)
        colour_white = (255, 255, 255)
        colour_green = (0, 255, 0)
        colour_red = (255, 0, 0)

        screen_width, screen_height = (1280, 720)
        option_width, option_height, option_space = self.size_of_option(
                                                screen_width, screen_height)
        x_coordinate = 0
        pygame.draw.rect(self._screen, colour_red, pygame.Rect(
            (screen_width / 2 - option_width/2), x_coordinate,
            option_width, option_height))
        self.message_display("MENU", 30, screen_width/2,
                             x_coordinate, colour_green)
        x_coordinate += option_height + option_space
        for i in self._options:
            pygame.draw.rect(self._screen, colour_red, pygame.Rect(
                (screen_width / 2 - option_width/2), x_coordinate,
                option_width, option_height))
            self.message_display(i.name, 30, screen_width/2,
                                 x_coordinate, colour_green)
            x_coordinate += option_height + option_space
        pygame.display.flip()

def test():
    print("lol")


if __name__ == "__main__":
    screen = pygame.display.set_mode((1280, 720),
                                     HWSURFACE | DOUBLEBUF | RESIZABLE)
    menu = Menu(screen, [("Resume", test), ("Options", test), ("Exit", test)])
    menu.display_menu()
    while True:
        for event in pygame.event.get():   # User did something
            if event.type == pygame.QUIT:
                sys.exit()
