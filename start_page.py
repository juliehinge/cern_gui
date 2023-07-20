import tkinter as tk      
from tkinter import ttk
from tkinter import *
from tkinter import font as tkfont  

class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="This is the start page", font=controller.title_font)
        label.grid(row=0, column=1, padx = (10), pady = (10))

        button1 = tk.Button(self, text="Get Started",
                            command=lambda: controller.show_frame("PageOne"))
        button1.grid(row=3, column=1, padx = (10), pady = (10))

    
        self.image = PhotoImage(file = "gui_figure1.png")
        self.image = self.image.subsample(3, 3) 
        img = tk.Label(self, image = self.image)
        img.grid(row=1, column=0, columnspan=3, padx = 10)
       
