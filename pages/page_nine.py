
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import tkinter as tk      
from tkinter import *
import matplotlib
matplotlib.use('TkAgg')  # Backend of matplotlib for tkinter
from matplotlib.figure import Figure
from function1 import default2
from p import Pages
from functions.map_mag_field import trajectory


class PageNine(tk.Frame):


    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
    
        # Binding to an event that passes the user defined variables once this page is opened to avoid having empty values passed back.
        self.bind("<<ShowFrame>>", self.pasvariable)

        # Create "Back" button
        back_button = tk.Button(self, text="Go back", 
                                command=lambda: controller.show_frame("PageEight"))
        back_button.pack()


        # Create a Frame
        self.frame = tk.Frame(self)
        self.frame.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        # Initialize a blank Figure and put it on tkinter frame
        self.fig = Figure(figsize=(5, 5), dpi=100)  # creating a blank figure
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame)  # linking figure with the FigureCanvasTkAgg
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    
        self.is_tool_bar = 0

    def pasvariable(self, event=None):
    

        # Getting the user defined variables from the Pages module
        A = Pages.alpha_list
        li = Pages.vector_list
        R = Pages.radius


        self.fig, ax = default2(A, li, R)  
        self.canvas.figure = self.fig  # Update the figure associated with the canvas
        self.canvas.draw()  # Redraw the canvas to reflect changes


        self.toolbar = NavigationToolbar2Tk(self.canvas, self.frame)
        self.toolbar.update()

