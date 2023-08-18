import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import font as tkfont

class StartPage(tk.Frame):

    def __init__(self, parent, controller, image_path):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # Adding a label to the frame and putting it on the grid
        tk.Label(self, text="Let's get started", font=controller.title_font).grid(row=0, column=1,pady=(10))

        # Adding a get started button that takes the user to the first page
        tk.Button(self, text="Get Started", command=lambda: controller.show_frame("PageOne")).grid(row=3, column=1, padx=(10), pady=(10))
        tk.Label(self, text="Julie Hinge").grid(row=3, column=2, sticky='e', pady=(10))

        # Using the provided image_path to load the image
        self.image = PhotoImage(file=image_path)
        self.image = self.image.subsample(3, 3) 
        img = tk.Label(self, image=self.image)
        img.grid(row=1, column=0, columnspan=3, padx=10)
