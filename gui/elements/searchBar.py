import ttkbootstrap as ttk
from ttkbootstrap.constants import *

class SearchBar:
    def __init__(self, root, data, app):
        self.root = root
        self.data = data
        self.app = app
        
        
        INP_SearchBar = ttk.Entry(self.app.FRAME_top, textvariable=self.app.searchVar, font=("Arial", 14))
        INP_SearchBar.pack(fill=X, padx=10, pady=5)