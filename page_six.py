from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import tkinter as tk      
from tkinter import ttk
from tkinter import *
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg')  # Backend of matplotlib for tkinter
from matplotlib.figure import Figure
import seaborn as sns
import pandas as pd
from function1 import default
from p import Pages

class PageSix(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
    

        self.bind("<<ShowFrame>>", self.pasvariable)

        # Create "Back" button
        back_button = tk.Button(self, text="Go back", 
                                command=lambda: controller.show_frame("PageFive"))
        back_button.pack()

        # Create a Frame
        self.frame = tk.Frame(self)
        self.frame.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        # Initialize a blank Figure and put it on tkinter frame
        
        self.fig = Figure(figsize=(5, 5), dpi=100)  # creating a blank figure
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame)  # linking figure with the FigureCanvasTkAgg
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)



    def pasvariable(self, event=None):
    
   

        A = Pages.alpha_list
        li = Pages.vector_list
        R = Pages.radius
        print(A, li, R)
        
        self.fig = default(A, li, R)  
        self.canvas.figure = self.fig  # Update the figure associated with the canvas
        self.canvas.draw()  # Redraw the canvas to reflect changes


