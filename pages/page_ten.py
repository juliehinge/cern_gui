from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import tkinter as tk      
from tkinter import *
import matplotlib
matplotlib.use('TkAgg')  # Backend of matplotlib for tkinter
from matplotlib.figure import Figure
from p import Pages
from functions.optimization2 import fmin
from functions.map_mag_field import display_magnetic_fild

class PageTen(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
    
        # Binding to an event that passes the user defined variables once this page is opened to avoid having empty values passed back.
        self.bind("<<ShowFrame>>", self.pasvariable)

        # Create "Back" button
        back_button = tk.Button(self, text="Go back", 
                                command=lambda: controller.show_frame("PageFifteen"))
        back_button.pack()


        # Create a Frame
        self.frame = tk.Frame(self)
        self.frame.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        # Initialize a blank Figure and put it on tkinter frame
        self.fig = Figure(figsize=(5, 5), dpi=100)  # creating a blank figure
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame)  # linking figure with the FigureCanvasTkAgg
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        self.is_toolbar = 0

    def pasvariable(self, event=None):
    
        # Getting the user defined variables from the Pages module
        x_min = float(Pages.x_min)         
        x_max = float(Pages.x_max)      
        y_min = float(Pages.y_min)
        y_max = float(Pages.y_max)
  

        optimized_A, optimized_li, average_beam_size, average_beam_disparity, beam_dif = fmin()

    
        # Calling the function that makes the plot and putting it on the GUI        
        self.fig, ax, _ = display_magnetic_fild(optimized_A, optimized_li, Pages.radius, plot_trajectory=True, custom_axis=True)  
        self.canvas.figure = self.fig  # Update the figure associated with the canvas
        self.canvas.draw()  # Redraw the canvas to reflect changes


        if self.is_toolbar == 0: # To avoid putting two zoom bars on the page
            self.toolbar = NavigationToolbar2Tk(self.canvas, self.frame)
            self.toolbar.update()
            self.is_toolbar += 1

            beams_size = tk.Label(self, text=f"Average Beam Size is: {average_beam_size}")
            beams_size.pack(anchor='w', padx=10, pady=(5, 0))

            beam_disparity = tk.Label(self, text=f"Average Beam Disperity is: {average_beam_disparity}")
            beam_disparity.pack(anchor='w', padx=10, pady=(0, 5))


            optimized_li_label = tk.Label(self, text=f"Angle between innermost and outermost beam: {beam_dif}")
            optimized_li_label.pack(anchor='w', padx=10, pady=(0, 5))

