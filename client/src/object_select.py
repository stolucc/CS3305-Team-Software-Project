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
