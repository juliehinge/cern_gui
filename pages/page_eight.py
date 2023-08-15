import tkinter as tk      
from tkinter import *
from tkinter import ttk
from p import Pages



class PageFifteen(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        tk.Label(self, text="*It may take some time for the optimization to run").grid(row=8, column=0, pady=10, sticky='e')


        #Labels for instructions
        tk.Label(self, text="Input bounds to change X and Y axis in beam tracking plot:", font = ("bold", 15)).grid(row=11, column=0, padx=10,pady=10, columnspan=3, sticky='w', )
    
        tk.Label(self, text="X-min:").grid(row=12, column=0, pady=10, sticky='e')
        tk.Label(self, text="X-max:").grid(row=13, column=0, pady=10, sticky='e')
        tk.Label(self, text="Y-min:").grid(row=12, column=2, pady=10, sticky='w', )
        tk.Label(self, text="Y-max:").grid(row=13, column=2, pady=10, sticky='w', )

        # Entry boxes set up
        self.x_min = ttk.Entry(self, width=5); self.x_min.grid(row=12, column=1, pady=10, sticky='w', )
        self.x_max = ttk.Entry(self, width=5); self.x_max.grid(row=13, column=1, pady=10, sticky='w', )
        self.y_min = ttk.Entry(self, width=5); self.y_min.grid(row=12, column=3, pady=10, sticky='w', )
        self.y_max = ttk.Entry(self, width=5); self.y_max.grid(row=13, column=3, pady=10, sticky='w', )




        button1 = ttk.Button(self, text="Back",
                            command=lambda: controller.show_frame("PageFifteen"))
        button1.grid(row=14, column=0,  pady = (10), sticky='e')


        button1 = ttk.Button(self, text="Ok",
                            command=lambda: self.open_zoomed_view())
        button1.grid(row=14, column=1,  pady = (10), sticky='w')

        # Warning text setup
        self.warning_text = tk.StringVar(self, value=' ')
        self.text = ttk.Label(self, textvariable = self.warning_text, foreground ="red").grid(row=9, column=0,pady = 5, columnspan=3)
        


    def open_zoomed_view(self):
        try:
            Pages.x_min = float(self.x_min.get())        
            Pages.x_max = float(self.x_max.get())      
            Pages.y_min = float(self.y_min.get())
            Pages.y_max = float(self.y_max.get())
            # Opening the zoomed in magnetic field plot
            self.controller.show_frame("PageTen")

        except ValueError:  # This will catch if the conversion to float fails (i.e., the entry is not a number)
            self.warning_text.set("Please make sure all entries are real numbers")
