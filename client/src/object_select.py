"""Module for menu to select object options."""
import pygame
import sys
from menu import Menu, MenuOption


class SelectMenu(Menu):
    """A class for the Select Menu."""

    def __init__(self, screen):
        """
        Create a new Select Menu.

        :param screen: A surface object that the menu will be displayed on
        """
        self._screen = screen
        self._screen_width = self._screen.get_width()
        self._screen_height = self._screen.get_height()
        self._background_colour = (74, 74, 74)
        self._border = (63, 142, 252)
        self._text_colour = (0, 0, 0)
        self._text_size = 20
        self._options = []
        self._pos = (0, 0)

    def display_menu(self):
        """
        Display the Select Menu.

        :param pos: The position the menu will start displaying.
        :param options: A list of tuples that have a name and a function.

        :return: True to represent that a menu is displayed.
        """
        if len(self._options) < 1:
            return False
        x_coordinate = self._pos[0]
        y_coordinate = self._pos[1]
        option_width, option_height = 170, 40
        self._start = []
        self._end = []
        if x_coordinate > self._screen_width/2:
            x_coordinate -= option_width
        if y_coordinate > self._screen_height/2:
            for i in range(len(self._options)-1, -1, -1):
                option_block = pygame.Rect(
                    x_coordinate, y_coordinate-option_height,
                    option_width, option_height)
                self.draw_option(option_block, self._options[i].name)
                self._start = [(x_coordinate,
                                y_coordinate-option_height)] + self._start
                self._end = [(x_coordinate + option_width,
                              y_coordinate)] + self._end
                y_coordinate -= option_height
        else:
            for i in range(len(self._options)):
                option_block = pygame.Rect(
                    x_coordinate, y_coordinate,
                    option_width, option_height)
                self.draw_option(option_block, self._options[i].name)
                self._start += [(x_coordinate, y_coordinate)]
                self._end += [(x_coordinate + option_width,
                               y_coordinate + option_height)]
                y_coordinate += option_height
        pygame.display.flip()
        return True

    def set_options(self, pos, options):
        """Set options to be displayed."""
        self._options = []
        self._pos = pos
        for i in options:
            if i is not None:
                self._options += [MenuOption(i[0], i[1])]


if __name__ == "__main__":
    screen = pygame.display.set_mode((1280, 720))
    pygame.font.init()
    isMenu = False

    def test():
        """Test Function."""
        print("test")

    menu = SelectMenu(screen)
    while True:
        for event in pygame.event.get():   # User did something
            screen.fill((0, 0, 0))
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                print(pos)
                if isMenu is False:
                    menu.set_options(pos, [("Move", test),
                                           ("Upgrade", test),
                                           ("Help", test),
                                           ("Exit", sys.exit)])
                    isMenu = menu.display_menu()
                else:
                    isMenu = menu.menu_click(pos)
                    if not isMenu:
                        screen.fill((0, 0, 0))
                        pygame.display.flip()
