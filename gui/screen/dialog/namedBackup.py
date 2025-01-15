"""
GameSaveVault - A tool for managing and backing up game save files.

Copyright (C) 2025 Julian Stiebler (stblr)

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>.

GitHub Repository: https://github.com/JulianStiebler/GameSaveVault
GitHub License: GNU GENERAL PUBLIC LICENSE Version 3, 29 June 2007
GitHub License File: https://github.com/JulianStiebler/GameSaveVault/blob/main/LICENSE

Last Edited: 16.01.2025
"""

import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from datetime import datetime
import tkinter as tk
from tkinter import messagebox
import os

class NamedBackupDialog:
    def __init__(self, parent, data, targetPath):
        self.result = None  # To store the final result
        self.data = data
        self.targetPath = targetPath
        self.dialog = ttk.Toplevel(parent)
        self.dialog.title("Custom Backup Name")
        self.dialog.geometry("400x250")  # Increased height to accommodate the warning label
        self.dialog.resizable(False, False)
        self.dialog.transient(parent)
        self.dialog.grab_set()

        # Add dialog widgets
        self.FRAME_main = ttk.Frame(self.dialog, padding=20)
        self.FRAME_main.pack(fill=BOTH, expand=True)

        # Custom name label and entry
        self.LBL_name = ttk.Label(self.FRAME_main, text="Enter a custom backup name:", font=("Arial", 12))
        self.LBL_name.pack(anchor=W, pady=(0, 5))

        self.INP_name = ttk.Entry(self.FRAME_main, font=("Arial", 12))
        self.INP_name.pack(fill=X, pady=(0, 10))

        # Add Timestamp checkbox
        self.CHK_timestamp_value = tk.BooleanVar(value=False)
        self.CHK_timestampBox = ttk.Checkbutton(self.FRAME_main, text="Add Timestamp", variable=self.CHK_timestamp_value, bootstyle="secondary")
        self.CHK_timestampBox.pack(anchor=W, pady=(0, 15))

        # Warning label (initially hidden, use pack_forget to hide it)
        self.LBL_warning = ttk.Label(self.FRAME_main, text="Invalid characters in the name!", font=("Arial", 10), bootstyle="warning")
        self.LBL_warning.pack(fill=X, pady=(0, 5))  # You can initially pack it if you want to show later.
        self.LBL_warning.pack_forget()

        # OK and Cancel buttons
        self.FRAME_buttons = ttk.Frame(self.dialog)
        self.FRAME_buttons.pack(fill=X, pady=5)

        self.BTN_okay = ttk.Button(self.FRAME_buttons, text="OK", command=self.__buttonOkay, bootstyle="success", state=DISABLED)
        self.BTN_okay.pack(side=RIGHT, padx=5)

        self.BTN_cancel = ttk.Button(self.FRAME_buttons, text="Cancel", command=self.__buttonCancel, bootstyle="danger")
        self.BTN_cancel.pack(side=RIGHT, padx=5)

        # Default focus on the entry
        self.INP_name.focus()

        # Bind the entry field to the validation function
        self.INP_name.bind("<KeyRelease>", self.__validateName)

        # Wait for the dialog to close
        self.dialog.wait_window()

    def __validateName(self, event):
        name = self.INP_name.get().strip()

        if name:  # If name is not empty, we check for invalid characters
            if self.data.utility.sanitizeFolderName_contains(name):
                self.BTN_okay.config(state=DISABLED)  # Disable the OK button
                if self.LBL_warning.winfo_ismapped() == 0:  # Check if the label is not already shown
                    self.LBL_warning.pack(fill=X, pady=(0, 5))  # Show the warning label
            else:
                self.BTN_okay.config(state=NORMAL)  # Enable the OK button
                if self.LBL_warning.winfo_ismapped() == 1:  # Check if the label is already shown
                    self.LBL_warning.pack_forget()  # Hide the warning label
        else:
            # If name is empty, hide the warning and disable OK button
            self.BTN_okay.config(state=DISABLED)
            if self.LBL_warning.winfo_ismapped() == 1:  # Check if the label is mapped (visible)
                self.LBL_warning.pack_forget()  # Hide the warning label

    def __buttonOkay(self):
        # Get user input
        timestamp = self.data.getTimestamp()
        name = self.INP_name.get().strip()
        if name:  # Ensure name is not empty
            if self.CHK_timestamp_value.get():
                # Add the timestamp if checkbox is checked
                fileName = f"{name}-{timestamp}.zip"
            else:
                fileName = f"{name}.zip"

            targetPath = os.path.join(self.targetPath, fileName)
            
            # Check if file exists
            if os.path.exists(targetPath):
                overwrite = messagebox.askyesno(
                    "File Exists",
                    f"The file '{fileName}' already exists. Do you want to overwrite it?"
                )
                if not overwrite:
                    # If user chooses not to overwrite, do nothing and keep the dialog open
                    return

            # If file doesn't exist or overwrite is confirmed
            self.result = fileName
            self.dialog.destroy()
        else:
            # Show a warning if the name is empty
            messagebox.showwarning("Invalid Input", "The name cannot be empty.")

    def __buttonCancel(self):
        self.result = None
        self.dialog.destroy()
