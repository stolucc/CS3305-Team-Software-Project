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

    def display_menu(self, pos, options):
        """
        Display the Select Menu.

        :param pos: The position the menu will start displaying.
        :param options: A list of tuples that have a name and a function.
        """
        background_colour1 = (63, 142, 252)
        background_colour2 = (73, 163, 26)
        text_colour = (255, 255, 255)
        text_size = 30
        self._options = []
        for i in options:
            self._options += [MenuOption(i[0], i[1])]
        x_coordinate = pos[0]
        y_coordinate = pos[1]
        option_width, option_height = self.size_of_option(400)
        self._start = []
        self._end = []
        for i in self._options:
            option_block = pygame.Rect(
                x_coordinate, y_coordinate,
                option_width, option_height)
            pygame.draw.rect(self._screen, background_colour2, option_block)
            pygame.draw.rect(self._screen, background_colour1, option_block, 3)
            self.message_display(i.name, text_size, x_coordinate +
                                 option_width/2, y_coordinate+5, text_colour)
            self._start += [(x_coordinate, y_coordinate)]
            self._end += [(x_coordinate + option_width,
                           y_coordinate + option_height)]
            y_coordinate += option_height
        pygame.display.flip()


if __name__ == "__main__":
    screen = pygame.display.set_mode((1280, 720))
    pygame.font.init()

    def test():
        """Test Function."""
        print("test")

    menu = SelectMenu(screen)
    #[("Resume", test), ("Options", test),("Help", test), ("Exit", sys.exit)]
    while True:
        for event in pygame.event.get():   # User did something
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                print(pos)
                menu.display_menu(pos, [("Resume", test), ("Options", test),
                                        ("Help", test), ("Exit", sys.exit)])
