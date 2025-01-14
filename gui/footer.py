import os
import ttkbootstrap as ttk
from ttkbootstrap.constants import BOTTOM, LEFT, RIGHT, X
from core.dataManager import DataManager


class Footer:
    def __init__(self, root, data):
        self.root = root
        self.data = data if data else DataManager()
        
        self.FRAME_footer = ttk.Frame(self.root)
        self.FRAME_footer.pack(side=BOTTOM, fill=X)
        
        links = {
            "GitHub": self.data.URL_GitHub,
            "Feature Request": self.data.URL_GitHub_FeatureRequest,
            "Bug Report": self.data.URL_GitHub_BugReport
        }
        
        for name, url in links.items():
            self.LBL_FooterLink = ttk.Label(self.FRAME_footer, text=name, font=("Arial", 10), anchor="center", bootstyle="light")
            self.LBL_FooterLink.pack(side=LEFT, padx=10)
            self.LBL_FooterLink.bind("<Button-1>", lambda e, url=url: os.startfile(url))
            self.LBL_FooterLink.bind("<Enter>", lambda e, label=self.LBL_FooterLink: label.config(foreground="#1E90FF"))
            self.LBL_FooterLink.bind("<Leave>", lambda e, label=self.LBL_FooterLink: label.config(foreground="#FFFFFF"))
            
        # Create non-clickable version label on the bottom right
        LBL_Version = ttk.Label(self.FRAME_footer, text=self.data.GITHUB_VERSION, font=("Arial", 10), anchor="e", bootstyle="light")
        LBL_Version.pack(side=RIGHT, padx=10)