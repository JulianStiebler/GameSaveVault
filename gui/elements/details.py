from .inner import ListBackupExplorer, ListFileExplorer

class Details:
    def __init__(self, root, data, app):
        self.root = root
        self.data = data
        self.app = app
        self.listBackup = ListBackupExplorer()
        self.listFiles = ListFileExplorer()