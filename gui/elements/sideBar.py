from .inner import ListGames

class SideBar:
    def __init__(self, root, data, app):
        self.root = root
        self.data = data
        self.app = app
        self.listGames = ListGames()