"""Module for menu to select object options."""
import pygame
import sys
from menu import Menu
from researchtree import ResearchTree


class TreeGUI(Menu):
    """Class for representing the visual of a tree."""

    def __init__(self, screen, tree):
        """
        Initialise attributes of TreeGUI.

        :param screen: A surface object to display the GUI on.
        :param tree: A research tree.
        """
        self._screen = screen
        self._screen_width = self._screen.get_width()
        self._screen_height = self._screen.get_height()
        self._background_colour = (74, 74, 74)
        self._border = (63, 142, 252)
        self._text_colour = (0, 0, 0)
        self._text_size = 20
        self._tree = tree
        self._start = []
        self._end = []
        self._unlockable_nodes = []
        self._wrapper = [(self._screen.get_width()-700)/2, 100,
                         ((self._screen.get_width()-700)/2) + 700, 100 + 500]

    def display_menu(self):
        """Display the menu and save it to the object."""
        self._start = []
        self._end = []
        self._unlockable_nodes = []
        option_width, option_height = 150, 40
        wrapper_x, wrapper_y = self.draw_background()
        x_coordinate = 25 + wrapper_x
        y_coordinate = 50 + wrapper_y
        branches = self._tree.branches
        unlockable = self._tree.unlockable_nodes()
        unlocked = self._tree.unlocked_nodes()
        branch_order = ["Worker", "Archer", "Swordsman", "Win"]
        for branch in branch_order:
            if branch == "Win":
                x_coordinate = 275 + wrapper_x
                y_coordinate = 400 + wrapper_y
            for i in range(len(branches[branch])):
                name = branch + " " + str(i+1)
                if branch == "Win":
                    name = branch
                option_block = pygame.Rect(
                    x_coordinate, y_coordinate,
                    option_width, option_height)
                node = branches[branch][i]
                if node in unlocked:
                    self.draw_option(option_block, name)
                elif node in unlockable:
                    self.draw_locked(option_block, name,
                                     node.unlock_cost)
                    self._unlockable_nodes += [node]
                    self._start += [(x_coordinate, y_coordinate)]
                    self._end += [(x_coordinate + option_width,
                                   y_coordinate + option_height)]
                y_coordinate += 100
            x_coordinate += 250
            y_coordinate = 50 + wrapper_y
        pygame.display.flip()

    def draw_locked(self, block, name, cost):
        """
        Draw a block for a locked menu option.

        :param block: A Rect object.
        :param name: The name the block displays.
        """
        locked_background = (0, 0, 0)
        locked_border = (255, 0, 0)
        locked_text = (255, 255, 255)
        pygame.draw.rect(self._screen, locked_background, block)
        pygame.draw.rect(self._screen, locked_border, block, 3)
        self.message_display(name, self._text_size, block.x +
                             block.width/2, block.y +
                             ((block.height-self._text_size-10)/2),
                             locked_text)
        self.message_display("Cost: " + str(cost), self._text_size/2, block.x +
                             block.width/2, block.y +
                             ((block.height-self._text_size+30)/2),
                             locked_text)

    def draw_background(self):
        """Draw background for Tree."""
        self._wrapper
        block = pygame.Rect(
            self._wrapper[0], self._wrapper[1],
            self._wrapper[2], self._wrapper[3])
        pygame.draw.rect(self._screen, self._background_colour, block)
        pygame.draw.rect(self._screen, self._border, block, 3)
        return self._wrapper[0], self._wrapper[1]

    def menu_click(self, pos):
        """
        Unlock the clicked research.

        :param pos: A tuple of coordinates that represent where
                    the user clicked
        """
        for i in range(len(self._unlockable_nodes)):
            if pos[0] >= self._start[i][0] and pos[0] <= self._end[i][0]:
                if pos[1] >= self._start[i][1] and pos[1] <= self._end[i][1]:
                    node = self._unlockable_nodes[i]
                    self._tree.unlock_node(node.id, node.branch)
        if pos[0] <= self._wrapper[0] and pos[0] >= self._wrapper[2]:
            if pos[1] <= self._wrapper[1] and pos[1] >= self._wrapper[3]:
                return True
            else:
                return False
        else:
            return False


if __name__ == "__main__":
    screen = pygame.display.set_mode((1280, 720))
    pygame.font.init()

    def test():
        """Test Function."""
        print("test")

    tree = ResearchTree(None)
    menu = TreeGUI(screen, tree)
    menu.display_menu()
    while True:
        for event in pygame.event.get():   # User did something
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                menu.menu_click(pos)
                menu.display_menu()
