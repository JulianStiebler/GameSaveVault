from .inner import ListGames
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

class SideBar:
    def __init__(self, root, data, utility, app):
        self.root = root
        self.data = data
        self.utility = utility
        self.app = app

        # Treeview for the game list
        self.listGames = ListGames(self.root, self.data, self.utility, self.app)