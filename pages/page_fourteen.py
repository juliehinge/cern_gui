
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import tkinter as tk      
from tkinter import *
import matplotlib
matplotlib.use('TkAgg')  # Backend of matplotlib for tkinter
from matplotlib.figure import Figure
#from function1 import get_points, default, default2
from p import Pages
from functions.map_mag_field import display_magnetic_fild, trajectory
from functions.optimization2 import beam_diff, beam_disparity, exit_size



class PageFourteen(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
    
        # Binding to an event that passes the user defined variables once this page is opened to avoid having empty values passed back.
        self.bind("<<ShowFrame>>", self.pasvariable)

        # Create "Back" button
        back_button = tk.Button(self, text="Go back", 
                                command=lambda: controller.show_frame("PageEleven"))
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
        A = Pages.alpha_list
        li = Pages.vector_list
        R = Pages.radius


        # Calling the function that makes the plot and putting it on the GUI        
            # Get the beam results from the default2 function
        x, y, _, indices, dd = trajectory(A, li, R)


        # Extract list of filenames (inner keys)
        file_keys = list(x.keys())
        results_beam_sizes = [exit_size(x[file], y[file], indices[file]) for file in file_keys]
        # Computing average beam size
        average_beam_size = sum(results_beam_sizes) / len(results_beam_sizes)

        # Computing beam disparity
        results_beam_disparity = [beam_disparity(dd[file], indices[file]) for file in file_keys]
        average_beam_disparity = sum(results_beam_disparity) / len(results_beam_disparity)

        beam_d = beam_diff(dd, indices)

 

        self.fig, ax, _ = display_magnetic_fild(A, li, R, plot_trajectory=True)  
        self.canvas.figure = self.fig  # Update the figure associated with the canvas
        self.canvas.draw()  # Redraw the canvas to reflect changes



        if self.is_toolbar == 0:
            self.toolbar = NavigationToolbar2Tk(self.canvas, self.frame)
            self.toolbar.update()


            beams_size = tk.Label(self, text=f"Average Beam Size is: {average_beam_size} radians") # Putting this on the gui
            beams_size.pack(anchor='w', padx=10, pady=(5, 0))

            beam_d = tk.Label(self, text=f"Average Beam Disperity is: {average_beam_disparity} radians") # Putting this on the gui
            beam_d.pack(anchor='w', padx=10, pady=(0, 5))


            optimized_li_label = tk.Label(self, text=f"Angle between innermost and outermost beam: {beam_d} degrees") # Putting this on the gui
            optimized_li_label.pack(anchor='w', padx=10, pady=(0, 5))       
            self.is_toolbar += 1

        # Calling the function that makes the plot and putting it on the GUI        
        
