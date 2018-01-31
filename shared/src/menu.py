import pygame
from pygame.locals import *

class Menu_Option:

    def __init__(self, name, function):

        self._name = name
        self._function = function

    @property
    def name(self):
        return name

    def function(self):
        return self._function()

class Menu:

    def __init__(self, options):
        pass
