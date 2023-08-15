import tkinter as tk      
from tkinter import *
from tkinter import ttk
from p import Pages



class PageEight(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        tk.Label(self, text="Input parameters for specifying the beam", font = ("bold", 20)).grid(row=0, column=0, padx = (10), pady = (10), columnspan=3)
        ttk.Label(self, text="-"*100, foreground="grey").grid(row=1, column=0, pady = (10,0), columnspan = 5, sticky='w')




        ttk.Label(self, text="Please input the tracking size", font = ("bold", 15)).grid(row=8, column=0, padx=5, pady = (10,0), columnspan = 5, sticky='w')

        tk.Label(self, text="Tracking size (m)").grid(row=9, column=0, pady=10, sticky='e')       
        self.track = ttk.Entry(self, width=5); self.track.grid(row=9, column=1, pady=10, sticky='w', )




        button1 = ttk.Button(self, text="Back",
                            command=lambda: controller.show_frame("Options"))
        button1.grid(row=11, column=0,  pady = (10), sticky='e')


        button1 = ttk.Button(self, text="Ok",
                            command=lambda: self.open_next_frame())
        button1.grid(row=11, column=1,  pady = (10), sticky='w')



        # Warning text setup
        self.warning_text = tk.StringVar(self, value=' ')
        self.text = ttk.Label(self, textvariable = self.warning_text, foreground ="red").grid(row=12, column=0,pady = 5, columnspan=3)
        
        self.entryFlag = True




    def open_next_frame(self):
        """This function first calls the record params function to make sure everything is ok. If the option is manual, page two will be opened,
        if the option is CSV page three will be opened. If there is a mistake in the user input, the user will be informed"""

        user_mistake = True
        Pages.open_optimization = False
        try:
            size = float(self.track.get())
            Pages.tracking = size
            user_mistake = False

        except ValueError:
            self.warning_text.set("Please input a real number as the tracking size")
            user_mistake = True

        if user_mistake == False:
            self.controller.show_frame("PageEleven")
        else:
            self.warning_text.set("Please fill out the information correctly")


