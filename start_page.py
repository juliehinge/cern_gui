import tkinter as tk      
from tkinter import ttk
from tkinter import *
from tkinter import font as tkfont  

class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller # Initialising

        # Adding a label to the frame and putting it on the grid
        tk.Label(self, text="Let's get started", font=controller.title_font).grid(row=0, column=1, padx = (10), pady = (10))

        # Adding a get started button that takes the user to the first page
        tk.Button(self, text="Get Started", command=lambda: controller.show_frame("PageOne")).grid(row=3, column=1, padx = (10), pady = (10))


        # Calling the image, resizing it, and placing it on the grid
        self.image = PhotoImage(file = "gui_figure1.png")
        self.image = self.image.subsample(3, 3) 
        img = tk.Label(self, image = self.image)
        img.grid(row=1, column=0, columnspan=3, padx = 10)
       
