import tkinter as tk
from tkinter import font as tkfont
from tkinter import ttk
from p import Pages
import math

class PageFive(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label1 = tk.Label(self, text="Section for viewing magnetic field", font = ("bold", 20))
        label1.grid(row=0, column=0, padx = (10), pady = (10), columnspan=4)
      

        preview = ttk.Button(self, text="Preview",
                            command=lambda: controller.show_frame("PageSix"))
        preview.grid(row=1, column=1, padx=2,pady=10, sticky = 'e')

     

        ttk.Label(self, text="-"*80, foreground="grey").grid(row=3, column=0, pady = (10,0), columnspan = 5, sticky='w')

        #Labels for instructions
        tk.Label(self, text="Input bounds to display zoomed in magnetic field plot:", font = ("bold", 15)).grid(row=4, column=0, padx=10,pady=10, columnspan=3, sticky='w', )
    
        tk.Label(self, text="X-min:").grid(row=5, column=0, pady=10)
        tk.Label(self, text="X-max:").grid(row=6, column=0, pady=10)
        tk.Label(self, text="Y-min:").grid(row=5, column=2, pady=10, sticky='w', )
        tk.Label(self, text="Y-max:").grid(row=6, column=2, pady=10, sticky='w', )

        # Entry boxes set up
        self.x_min = ttk.Entry(self, width=5); self.x_min.grid(row=5, column=1, pady=10, sticky='w', )
        self.x_max = ttk.Entry(self, width=5); self.x_max.grid(row=6, column=1, pady=10, sticky='w', )
        self.y_min = ttk.Entry(self, width=5); self.y_min.grid(row=5, column=3, pady=10, sticky='w', )
        self.y_max = ttk.Entry(self, width=5); self.y_max.grid(row=6, column=3, pady=10, sticky='w', )



        # Button for returning back to page one
        button1 = ttk.Button(self, text="Back",
                            command=lambda: self.go_back())
        button1.grid(row=9, column=0,  pady = (10,20), sticky='e')

        # Button for opening the zoomed in frame
        button2 = ttk.Button(self, text="OK",
                            command=lambda: self.open_next_frame())
        button2.grid(row=7, column=1,  pady = (10), sticky='e')


        ttk.Label(self, text="-"*80, foreground="grey").grid(row=8, column=0, pady = (10,0), columnspan = 5, sticky='w')

        # Button for going to the tracking beam section
        button3 = ttk.Button(self, text="View Beam tracking",
                            command=lambda: self.open_tracking_frame())
        button3.grid(row=9, column=1, pady = (10,20), sticky='w', columnspan=2)






    def open_next_frame(self):
        # Getting the user defined variables from the pages module
        Pages.x_min = self.x_min.get()        
        Pages.x_max = self.x_max.get()       
        Pages.y_min = self.y_min.get()
        Pages.y_max = self.y_max.get()
        # Opening the zoomed in magnetic field plot
        self.controller.show_frame("PageSeven")

    


    def open_tracking_frame(self):
        # Opening the frame where users can input variables for tracking the beam
        self.controller.show_frame("PageEight")

    

    def go_back(self):
        if Pages.manual == True:
            self.controller.show_frame("PageTwo")
        else:
            self.controller.show_frame("PageFour")