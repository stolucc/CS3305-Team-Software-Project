"""Module for building main game menu."""
import pygame
import sys


class MenuOption:
    """A Class for a single menu option in a menu."""

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
        self._header = "Menu"

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

    def message_display(self, text, text_size, x_cord, y_cord, colour):
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
        TextRect.center = (x_cord, y_cord + text_size/2)
        self._screen.blit(TextSurf, TextRect)

    def size_of_option(self, width, height):
        """
        Calculate the size of the menu options.

        :param width: The width of the surface
        :param height: The height of the surface
        :return: return the width of the menu option (option_width)
                and the height (option_height)
        """
        option_height_space = 60
        option_height = 35
        option_width = width/2
        return option_width, option_height, option_height_space

    def display_menu(self):
        """Display the menu and save it to the object."""
        pygame.font.init()
        background_colour = (91, 185, 247)
        main_background_colour = (150, 150, 150)
        text_colour = (249, 243, 122)
        text_size = 30

        screen_width, screen_height = (1280, 720)
        option_width, option_height, option_space = self.size_of_option(
                                                screen_width, screen_height)
        y_coordinate = 0
        pygame.draw.rect(self._screen, main_background_colour, pygame.Rect(
            (screen_width/2 - screen_width/4), y_coordinate,
            screen_width/2, option_height))
        self.message_display(self._header, text_size, screen_width/2,
                             y_coordinate, text_colour)
        heading_space = 140 + option_space + option_height
        # Coordinates for where menu display starts.
        y_coordinate += heading_space
        x_coordinate = screen_width / 2 - option_width/2
        # Stores locations of where menu option is drawn.
        self._start = []
        self._end = []
        # Each Menu Option
        for i in self._options:
            option_block = pygame.Rect(
                x_coordinate, y_coordinate,
                option_width, option_height)
            pygame.draw.rect(self._screen, background_colour, option_block, 1)
            self.message_display(i.name, 30, x_coordinate + option_width/2,
                                 y_coordinate, text_colour)
            self._start += [(x_coordinate, y_coordinate)]
            self._end += [(x_coordinate + option_width,
                           y_coordinate + option_height)]
            y_coordinate += option_height + option_space
        pygame.display.flip()

    def menu_click(self, pos):
        """
        Run the function that the user has clicked.

        :param pos: A tuple of coordinates that represent where
                    the user clicked
        """
        for i in range(len(self._options)):
            if pos[0] >= self._start[i][0] and pos[0] <= self._end[i][0]:
                if pos[1] >= self._start[i][1] and pos[1] <= self._end[i][1]:
                    self._options[i].menu_function


if __name__ == "__main__":
    screen = pygame.display.set_mode((1280, 720))

    def test():
        """Test Function."""
        print("test")

    menu = Menu(screen, [("Resume", test), ("Options", test),
                         ("Halp", test), ("Exit", sys.exit)])
    menu.display_menu()
    while True:
        for event in pygame.event.get():   # User did something
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                print(pos)
                menu.menu_click(pos)
