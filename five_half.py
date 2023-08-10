import tkinter as tk
from tkinter import font as tkfont
from tkinter import ttk
from p import Pages
import math

class FiveHalf(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label1 = tk.Label(self, text="Go To:", font = ("bold", 20))
        label1.grid(row=0, column=0, padx = (10), pady = (10), columnspan=4)
      

        # Button for opening magnetic field preview
        preview = ttk.Button(self, text="Magnetic Field Preview", width=20,
                            command=lambda: controller.show_frame("PageSix"))
        preview.grid(row=1, column=1, padx=10,pady=10, sticky = 'w')

        # Section for viewing zoomed in magnetic field preview
        zoomed_preview = ttk.Button(self, text="Zoomed Magnetic Field Preview", width=20,
                            command=lambda: controller.show_frame("PageFive"))
        zoomed_preview.grid(row=2, column=1, padx=10,pady=10, sticky = 'w')

        # Section for beam tracking
        beam_tracking = ttk.Button(self, text="Beam Tracking", width=20,
                            command=lambda: controller.show_frame("PageEight"))
        beam_tracking.grid(row=3, column=1, padx=10,pady=10, sticky = 'w')

        # Section for beam Optimization
        beam_optimization = ttk.Button(self, text="Beam Optimization", width=20,
                            command=lambda: controller.show_frame("PageSix"))
        beam_optimization.grid(row=4, column=1, padx=10,pady=10, sticky = 'w')

       # Section for beam Optimization
        back = ttk.Button(self, text="Back", width=20,
                            command=lambda:self.go_back())
        back.grid(row=5, column=1, padx=10,pady=10, sticky = 'w')

     
     
    def go_back(self):
        if Pages.manual == True:
            self.controller.show_frame("PageTwo")
        else:
            self.controller.show_frame("PageFour")