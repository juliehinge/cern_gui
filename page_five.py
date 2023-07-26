import tkinter as tk
from tkinter import font as tkfont
from tkinter import ttk
from p import Pages
import math

class PageFive(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label1 = tk.Label(self, text="Section for plotting magnetic field", font = ("bold", 20))
        label1.grid(row=0, column=0, padx = (10), pady = (10), columnspan=4)
      

        preview = ttk.Button(self, text="Preview",
                            command=lambda: controller.show_frame("PageSix"))
        preview.grid(row=1, column=2, padx=2,pady=10, sticky = 'w')

        

        #Labels for instructions
        tk.Label(self, text="Input your own parameters:", font = ("bold", 15)).grid(row=3, column=0, pady=10, columnspan=3, sticky='w', )
    
        tk.Label(self, text="X-min:").grid(row=4, column=0, pady=10)
        tk.Label(self, text="X-max:").grid(row=5, column=0, pady=10)
        tk.Label(self, text="Y-min:").grid(row=4, column=2, pady=10, sticky='w', )
        tk.Label(self, text="Y-max:").grid(row=5, column=2, pady=10, sticky='w', )

       # self.x_min = ttk.Entry(self); self.x_min.grid(row=4, column=1, pady=10, sticky='w', )
        self.x_min = ttk.Entry(self, width=5); self.x_min.grid(row=4, column=1, pady=10, sticky='w', )
        self.x_max = ttk.Entry(self, width=5); self.x_max.grid(row=5, column=1, pady=10, sticky='w', )
        self.y_min = ttk.Entry(self, width=5); self.y_min.grid(row=4, column=3, pady=10, sticky='w', )
        self.y_max = ttk.Entry(self, width=5); self.y_max.grid(row=5, column=3, pady=10, sticky='w', )





        button1 = ttk.Button(self, text="Back",
                            command=lambda: controller.show_frame("PageOne"))
        button1.grid(row=6, column=0,  pady = (10), sticky='e')


        button2 = ttk.Button(self, text="OK",
                            command=lambda: self.open_next_frame())
        button2.grid(row=6, column=1,  pady = (10), sticky='w')



        self.warning_text = tk.StringVar(self, value=' ')
        self.text = ttk.Label(self, textvariable = self.warning_text, foreground ="red").grid(row=10, column=0,pady = 5, columnspan=3)
        




    def open_next_frame(self):
        Pages.x_min = self.x_min.get()        
        Pages.x_max = self.x_max.get()       
        Pages.y_min = self.y_min.get()
        Pages.y_max = self.y_max.get()
        self.controller.show_frame("PageSeven")

    
