import tkinter as tk      
from tkinter import *
from tkinter import ttk
from p import Pages



class PageTen(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        tk.Label(self, text="Input parameters for specifying the beam", font = ("bold", 20)).grid(row=0, column=0, padx = (10), pady = (10), columnspan=3)
        ttk.Label(self, text="-"*100, foreground="grey").grid(row=1, column=0, pady = (10,0), columnspan = 5, sticky='w')


        tk.Label(self, text="How would you like to input your list of particle directions and positions:", font = ("bold", 15)).grid(row=4, column=0,pady=(10,0),columnspan=3, sticky='w')


        # This is the setup for the checkboxes
        self.var1 = tk.IntVar()
        self.var2 = tk.IntVar()
        c1 = tk.Checkbutton(self, text='Manually',variable=self.var1, onvalue=1, offvalue=0, command=self.get_selection)
        c1.grid(row=5, column=1, padx=20, pady=(10,0),sticky='w')
        c2 = tk.Checkbutton(self, text='By CSV upload',variable=self.var2, onvalue=1, offvalue=0, command=self.get_selection)
        c2.grid(row=6, column=1, padx=20, pady=(0,10),sticky='w')


        ttk.Label(self, text="-"*100, foreground="grey").grid(row=7, column=0, pady = (10,0), columnspan = 5, sticky='w')

        ttk.Label(self, text="Please input the tracking size and charge of paricles").grid(row=8, column=0, pady = (10,0), columnspan = 5, sticky='w')

        tk.Label(self, text="Tracking size (m)").grid(row=9, column=0, pady=10, sticky='e')
        tk.Label(self, text="Charge of Particles (+/-)").grid(row=10, column=0, pady=10, sticky='e')

       
        self.track = ttk.Entry(self, width=5); self.track.grid(row=9, column=1, pady=10, sticky='w', )
        self.charge = ttk.Entry(self, width=5); self.charge.grid(row=10, column=1, pady=10, sticky='w', )




        button1 = ttk.Button(self, text="Back",
                            command=lambda: controller.show_frame("PageEight"))
        button1.grid(row=11, column=0,  pady = (10), sticky='e')


        button1 = ttk.Button(self, text="Ok",
                            command=lambda: self.open_next_frame())
        button1.grid(row=11, column=1,  pady = (10), sticky='w')



        # Warning text setup
        self.warning_text = tk.StringVar(self, value=' ')
        self.text = ttk.Label(self, textvariable = self.warning_text, foreground ="red").grid(row=12, column=0,pady = 5, columnspan=3)
        
        self.entryFlag = True
        self.method = False



    def get_selection(self):
        """This function is for making sure that the user only chose one checkbox for the manual vs.csv option. If they didn't the warning text and flags will be set"""
        if (self.var1.get() == 1) & (self.var2.get() == 0): # Getting the value of the checkbox: 1 = on, 0 = off )
            self.warning_text.set("")
            self.checkFlag = True
            self.method = False
        elif (self.var1.get() == 0) & (self.var2.get() == 1):
            self.warning_text.set("")
            self.checkFlag = True
            self.method = True
        elif (self.var1.get() == 0) & (self.var2.get() == 0):
            self.warning_text.set("Please choose an option")
            self.checkFlag = False
        else:
            self.warning_text.set("Please choose only on option")
            self.checkFlag = False





    def open_next_frame(self):
        """This function first calls the record params function to make sure everything is ok. If the option is manual, page two will be opened,
        if the option is CSV page three will be opened. If there is a mistake in the user input, the user will be informed"""
        print(self.entryFlag)

        if self.entryFlag == True and self.method == False:
            self.controller.show_frame("PageEleven")
        elif self.entryFlag == True and self.method == True:
            self.controller.show_frame("PageTwelve")
        else:
            self.warning_text.set("Please fill out the information correctly")


