import ttkbootstrap as ttk
from ttkbootstrap.constants import *

class ContextMenu:
    def __init__(self, root, data, app):
        self.root = root
        self.data = data
        self.app = app
        self.menu_bar = ttk.Menu(self.root)
        self._setup_menu()
        self.root.config(menu=self.menu_bar)

    def _setup_menu(self):
        # Program menu
        program_menu = ttk.Menu(self.menu_bar, tearoff=0)
        program_menu.add_command(label="Exit", command=self.root.quit)  # Placeholder Exit command
        program_menu.add_command(label="Reload Epic Library", command=self.data.detectSystem.initEpicLibrary)
        self.menu_bar.add_cascade(label="Program", menu=program_menu)
        
        # Add more menus if needed
        # Example: Help menu
        help_menu = ttk.Menu(self.menu_bar, tearoff=0)
        help_menu.add_command(label="About", command=self._show_about)
        self.menu_bar.add_cascade(label="Help", menu=help_menu)

    def _show_about(self):
        # Placeholder for About functionality
        ttk.messagebox.showinfo("About", "This is a sample application.")
