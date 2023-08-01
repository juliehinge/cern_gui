import tkinter as tk
from tkinter import font as tkfont
from tkinter import ttk
from p import Pages
import re


class PageEight(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

   
        label1 = tk.Label(self, text="Section for tracking particle beam", font = ("bold", 20))
        label1.grid(row=0, column=0, padx = (10), pady = (10), columnspan=4)
      

        #Labels for instructions
        tk.Label(self, text="Input your own parameters:", font = ("bold", 15)).grid(row=2, column=0, pady=10, columnspan=3, sticky='w', )

        tk.Label(self, text="Position of Point:").grid(row=4, column=0, pady=10)
        tk.Label(self, text="Velocity of point:").grid(row=4, column=2, pady=10)
        tk.Label(self, text="Tracking size (m)").grid(row=5, column=0, pady=10, sticky='w', )
        tk.Label(self, text="Charge of Particles (+/-)").grid(row=5, column=2, pady=10, sticky='w', )

        self.point = ttk.Entry(self, width=5); self.point.grid(row=4, column=1, pady=10, sticky='w', )
        self.vel = ttk.Entry(self, width=5); self.vel.grid(row=4, column=3, pady=10, sticky='w', )
        self.track = ttk.Entry(self, width=5); self.track.grid(row=5, column=1, pady=10, sticky='w', )
        self.charge = ttk.Entry(self, width=5); self.charge.grid(row=5, column=3, pady=10, sticky='w', )



        button1 = ttk.Button(self, text="Back",
                            command=lambda: controller.show_frame("PageSeven"))
        button1.grid(row=7, column=0,  pady = (10), sticky='e')



        button1 = ttk.Button(self, text="Ok",
                            command=lambda: self.check())
        button1.grid(row=7, column=1,  pady = (10), sticky='e')

        # Warning text setup
        self.warning_text = tk.StringVar(self, value=' ')
        self.text = ttk.Label(self, textvariable = self.warning_text, foreground ="red").grid(row=8, column=0,pady = 5, columnspan=3)
        




    def check(self):
        flag = False
        for i in (self.point.get(), self.vel.get()):
            try:
                parts = i.split(',')
                # There should be exactly 2 parts
                if len(parts) != 2:
                    return False
                # Both parts should be convertible to a float 
                float(parts[0])
                float(parts[1])
                self.warning_text.set("")
                flag = True
            except ValueError:
                self.warning_text.set("Please make sure that the point and velocity are two numbers seperated by a comma")
                flag = False

        try:
            str(self.charge.get())
            float(self.track.get())
            self.warning_text.set("")
            flag = True
        except ValueError:
            self.warning_text.set("Please make sure that the charge is +/- and the tracking size is a valid float")
            flag = False

        if flag == True:
            Pages.tracking = float(self.track.get())
            Pages.charge = str(self.charge.get())
            Pages.P = [float(num) for num in re.split(',| ', self.point.get()) if num]
            Pages.D = [float(num) for num in re.split(',| ', self.vel.get()) if num]

            self.controller.show_frame("PageNine")
