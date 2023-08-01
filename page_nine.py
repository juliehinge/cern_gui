
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk      
from tkinter import *
import matplotlib
matplotlib.use('TkAgg')  # Backend of matplotlib for tkinter
from matplotlib.figure import Figure
from function1 import get_points, default, default2
from p import Pages



class PageNine(tk.Frame):


    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
    
        # Binding to an event that passes the user defined variables once this page is opened to avoid having empty values passed back.
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
    

        # Getting the user defined variables from the Pages module
       # P = Pages.P # Getting the coorinates of the point
       # D = Pages.D # Getting the direction of the point
       # charge = Pages.charge # Getting the charge
       # tracking = Pages.tracking # Getting the tracking size
   


        A = Pages.alpha_list
        li = Pages.vector_list
        R = Pages.radius

      
        # Calling the function that makes the plot and putting it on the GUI        
        self.fig, ax = default2(A, li, R)  
        self.canvas.figure = self.fig  # Update the figure associated with the canvas
        self.canvas.draw()  # Redraw the canvas to reflect changes


