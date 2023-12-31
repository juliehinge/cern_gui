import tkinter as tk
from tkinter import font as tkfont
from tkinter import ttk
from p import Pages
import math

class PageFive(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label1 = tk.Label(self, text="Section for viewing Zoomed in magnetic field", font = ("bold", 20))
        label1.grid(row=0, column=0, padx = (10), pady = (10), columnspan=4)
      

        ttk.Label(self, text="-"*80, foreground="grey").grid(row=1, column=0, pady = (10,0), columnspan = 5, sticky='w')

        #Labels for instructions
        tk.Label(self, text="Input bounds to display zoomed in magnetic field plot:", font = ("bold", 15)).grid(row=2, column=0, padx=10,pady=10, columnspan=3, sticky='w', )
    
        tk.Label(self, text="X-min:").grid(row=3, column=0, pady=10)
        tk.Label(self, text="X-max:").grid(row=4, column=0, pady=10)
        tk.Label(self, text="Y-min:").grid(row=3, column=2, pady=10, sticky='w', )
        tk.Label(self, text="Y-max:").grid(row=4, column=2, pady=10, sticky='w', )

        # Entry boxes set up
        self.x_min = ttk.Entry(self, width=5); self.x_min.grid(row=3, column=1, pady=10, sticky='w', )
        self.x_max = ttk.Entry(self, width=5); self.x_max.grid(row=4, column=1, pady=10, sticky='w', )
        self.y_min = ttk.Entry(self, width=5); self.y_min.grid(row=3, column=3, pady=10, sticky='w', )
        self.y_max = ttk.Entry(self, width=5); self.y_max.grid(row=4, column=3, pady=10, sticky='w', )



        # Button for returning back to page one
        button1 = ttk.Button(self, text="Back",
                            command=lambda: controller.show_frame("Options"))
        button1.grid(row=5, column=0,  pady = (10), sticky='e')

        # Button for opening the zoomed in frame
        button2 = ttk.Button(self, text="OK",
                            command=lambda: self.open_next_frame())
        button2.grid(row=5, column=1,  pady = (10), sticky='e')

     



    def open_next_frame(self):
        # Getting the user defined variables from the pages module
        Pages.x_min = self.x_min.get()        
        Pages.x_max = self.x_max.get()       
        Pages.y_min = self.y_min.get()
        Pages.y_max = self.y_max.get()
        # Opening the zoomed in magnetic field plot
        self.controller.show_frame("PageSeven")

    


    

