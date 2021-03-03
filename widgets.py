import tkinter as tk
from tkinter import filedialog as fd


class EntryWidget(tk.Frame):
    def __init__(self, parent, label, default=""):
        tk.Frame.__init__(self, parent)

        self.entry_frame = tk.Frame(
            self, width=1000, bg="green")
        self.entry_frame.grid(row=1, column=2)

        self.label = tk.Label(self.entry_frame, text=label, anchor="w")
        self.entry = tk.Entry(self.entry_frame)
        self.entry.insert(0, default)

        # self.label.pack(side="top", fill="x")
        # self.entry.pack(side="bottom", fill="x", padx=4)
        self.label.grid(row=1, column=1, sticky="NSEW")
        self.entry.grid(row=1, column=2)

    def get(self):
        return self.entry.get()


class OptionWidget(tk.Frame):
    def __init__(self, parent, label, options=[]):
        tk.Frame.__init__(self, parent)

        self.grid_label = tk.Frame(self)
        self.grid_entry = tk.Frame(self)

        self.grid_label.grid(row=1, column=1)
        self.grid_entry.grid(row=1, column=2)

        self.selected_value = tk.StringVar(self)

        self.label = tk.Label(self.grid_label, text=label, anchor="w")
        self.options = tk.OptionMenu(
            self.grid_entry, self.selected_value, *options)

        # self.label.pack(side="top", fill="x")
        # self.options.pack(side="bottom", fill="x", padx=4)
        self.label.grid(row=1, column=1, sticky="E")
        self.options.grid(row=1, column=2, sticky="E")

    def get(self):
        return self.selected_value.get()


class DirectoryWidget(tk.Frame):
    def __init__(self, parent, label):
        tk.Frame.__init__(self, parent)
        # Holds the path selected by the browser
        self.filename = ""

        self.frame = tk.Frame(self)
        self.frame.grid(row=2, column=1)

        self.filename_display = tk.Label(self.frame)
        self.filename_display["text"] = self.filename

        self.button = tk.Button(
            self.frame, text=label, command=self.browse_folders
        )

        self.button.grid(row=1, column=1)
        self.filename_display.grid(row=2, column=1)

    def get(self):
        return self.filename

    def browse_folders(self):
        """Handles the folder selection and
        updating label elements with new info
        """

        folder = fd.askdirectory(
            initialdir="./", title="Select image directory")

        self.filename = folder
        self.filename_display["text"] = folder
