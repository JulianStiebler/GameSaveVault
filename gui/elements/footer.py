import os
import ttkbootstrap as ttk
from ttkbootstrap.constants import BOTTOM, LEFT, RIGHT, X
from core.enums import AppConfigGithub, AppConfig


class Footer:
    def __init__(self, root, data, app):
        self.root = root
        self.data = data
        self.app = app
        
        self.FRAME_footer = ttk.Frame(self.root)
        self.FRAME_footer.pack(side=BOTTOM, fill=X)
        
        links = {
            "GitHub": AppConfigGithub.GITHUB_URL_ORIGIN.value,
            "Feature Request": AppConfigGithub.GITHUB_URL_FEATUREREQUEST.value,
            "Bug Report": AppConfigGithub.GITHUB_URL_BUGREPORT.value
        }
        
        for name, url in links.items():
            self.LBL_FooterLink = ttk.Label(self.FRAME_footer, text=name, font=("Arial", 10), anchor="center", bootstyle="light")
            self.LBL_FooterLink.pack(side=LEFT, padx=10)
            self.LBL_FooterLink.bind("<Button-1>", lambda e, url=url: os.startfile(url))
            self.LBL_FooterLink.bind("<Enter>", lambda e, label=self.LBL_FooterLink: label.config(foreground="#1E90FF"))
            self.LBL_FooterLink.bind("<Leave>", lambda e, label=self.LBL_FooterLink: label.config(foreground="#FFFFFF"))
            
        # Create non-clickable version label on the bottom right
        LBL_Version = ttk.Label(self.FRAME_footer, text=AppConfig.VERSION.value, font=("Arial", 10), anchor="e", bootstyle="light")
        LBL_Version.pack(side=RIGHT, padx=10)