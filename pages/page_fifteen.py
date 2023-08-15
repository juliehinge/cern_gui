import tkinter as tk      
from tkinter import *
from tkinter import ttk
from p import Pages



class PageFifteen(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        tk.Label(self, text="Input parameters for optimization of the beam", font = ("bold", 20)).grid(row=0, column=0, padx = (10), pady = (10), columnspan=3)
        ttk.Label(self, text="-"*100, foreground="grey").grid(row=1, column=0, pady = (10,0), columnspan = 5, sticky='w')



        ttk.Label(self, text="Please input your ideal parameters", font = ("bold", 15)).grid(row=3, column=0, padx=5, pady = (10,0), columnspan = 5, sticky='w')

        tk.Label(self, text="Beam Angle").grid(row=4, column=0, pady=10, sticky='e')
        tk.Label(self, text="Average Beam Divergence").grid(row=5, column=0, pady=10, sticky='e')
        tk.Label(self, text="Average Beam Size").grid(row=6, column=0, pady=10, sticky='e')

        self.angle = ttk.Entry(self, width=5); self.angle.grid(row=4, column=1, pady=10, sticky='w', )
        self.divergence = ttk.Entry(self, width=5); self.divergence.grid(row=5, column=1, pady=10, sticky='w', )
        self.size = ttk.Entry(self, width=5); self.size.grid(row=6, column=1, pady=10, sticky='w', )



        button1 = ttk.Button(self, text="Back",
                            command=lambda: controller.show_frame("PageEleven"))
        button1.grid(row=7, column=0,  pady = (10), sticky='e')


        button1 = ttk.Button(self, text="Ok",
                            command=lambda: self.open_next_frame())
        button1.grid(row=7, column=1,  pady = (10), sticky='w')


        tk.Label(self, text="*It may take some time for the optimization to run").grid(row=8, column=0, pady=10, sticky='w')

        # Warning text setup
        self.warning_text = tk.StringVar(self, value=' ')
        self.text = ttk.Label(self, textvariable = self.warning_text, foreground ="red").grid(row=8, column=0,pady = 5, columnspan=3)
        
        self.entryFlag = True
        self.method = False



        #Labels for instructions
        tk.Label(self, text="Input bounds to display zoomed in beam tracking plot:", font = ("bold", 15)).grid(row=9, column=0, padx=10,pady=10, columnspan=3, sticky='w', )
    
        tk.Label(self, text="X-min:").grid(row=10, column=0, pady=10)
        tk.Label(self, text="X-max:").grid(row=11, column=0, pady=10)
        tk.Label(self, text="Y-min:").grid(row=10, column=2, pady=10, sticky='w', )
        tk.Label(self, text="Y-max:").grid(row=11, column=2, pady=10, sticky='w', )

        # Entry boxes set up
        self.x_min = ttk.Entry(self, width=5); self.x_min.grid(row=10, column=1, pady=10, sticky='w', )
        self.x_max = ttk.Entry(self, width=5); self.x_max.grid(row=11, column=1, pady=10, sticky='w', )
        self.y_min = ttk.Entry(self, width=5); self.y_min.grid(row=10, column=3, pady=10, sticky='w', )
        self.y_max = ttk.Entry(self, width=5); self.y_max.grid(row=11, column=3, pady=10, sticky='w', )





        button1 = ttk.Button(self, text="Back",
                            command=lambda: controller.show_frame("PageEleven"))
        button1.grid(row=12, column=0,  pady = (10), sticky='e')


        button1 = ttk.Button(self, text="Ok",
                            command=lambda: self.open_zoomed_view())
        button1.grid(row=12, column=1,  pady = (10), sticky='w')


    def open_zoomed_view(self):
        Pages.x_min = self.x_min.get()        
        Pages.x_max = self.x_max.get()       
        Pages.y_min = self.y_min.get()
        Pages.y_max = self.y_max.get()
        # Opening the zoomed in magnetic field plot
        self.controller.show_frame("PageTen")




    def open_next_frame(self):
        try:
            # Get values from the entries
            angle_value = float(self.angle.get())
            divergence_value = float(self.divergence.get())
            size_value = float(self.size.get())

            # Check if values are positive and angle is not more than 180
            if (angle_value > 0 and angle_value <= 180) and divergence_value > 0 and size_value > 0:
                self.warning_text.set("")
                Pages.angle = angle_value
                Pages.beam_divergence = divergence_value
                Pages.size = size_value
                self.controller.show_frame("PageSixteen")

            else:
                self.warning_text.set("Please make sure all entries are postitive numbers and the angle is less than 180 degrees")
        except ValueError:  # This will catch if the conversion to float fails (i.e., the entry is not a number)
            self.warning_text.set("Please make sure all entries are postitive numbers and the angle is less than 180 degrees")



