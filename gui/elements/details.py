from .inner import ListBackupExplorer, ListFileExplorer

class Details:
    def __init__(self, root, data, utility, app):
        self.root = root
        self.data = data
        self.utility = utility
        self.app = app
        self.listBackup = ListBackupExplorer()
        self.listFiles = ListFileExplorer()