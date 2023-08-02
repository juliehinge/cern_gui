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

        tk.Label(self, text="Reference Point:").grid(row=2, column=0, pady=10, sticky='w')
        tk.Label(self, text="Reference Direction").grid(row=3, column=0, pady=10, sticky='w')
      
        self.ref_point = ttk.Entry(self, width=5); self.ref_point.grid(row=2, column=1, pady=10, sticky='w')
        self.ref_dir = ttk.Entry(self, width=5); self.ref_dir.grid(row=3, column=1, pady=10, sticky='w')



        tk.Label(self, text="How would you like to input your list of particle directions and positions:", font = ("bold", 15)).grid(row=4, column=0,pady=(10,0),columnspan=3, sticky='w')


        # This is the setup for the checkboxes
        self.var1 = tk.IntVar()
        self.var2 = tk.IntVar()
        c1 = tk.Checkbutton(self, text='Manually',variable=self.var1, onvalue=1, offvalue=0, command=self.get_selection)
        c1.grid(row=5, column=0, pady=(10,0), sticky='w')
        c2 = tk.Checkbutton(self, text='By CSV upload',variable=self.var2, onvalue=1, offvalue=0, command=self.get_selection)
        c2.grid(row=6, column=0, sticky='w', pady=(0,10))



        button1 = ttk.Button(self, text="Back",
                            command=lambda: controller.show_frame("PageEight"))
        button1.grid(row=7, column=0,  pady = (10), sticky='e')


        button1 = ttk.Button(self, text="Ok",
                            command=lambda: self.open_next_frame())
        button1.grid(row=7, column=1,  pady = (10), sticky='w')



        # Warning text setup
        self.warning_text = tk.StringVar(self, value=' ')
        self.text = ttk.Label(self, textvariable = self.warning_text, foreground ="red").grid(row=13, column=0,pady = 5, columnspan=3)
        
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



    def record_params(self):
        """This function ensures that the input are correct and returns them to the pages module"""
        for i in (self.ref_point.get(),self.ref_dir.get()):
            try:
                parts = i.split(',')
                # There should be exactly 2 parts
                if len(parts) != 2:
                    self.entryFlag = False
                # Both parts should be convertible to a float 
      
                self.warning_text.set("")
                self.entryFlag = True
                
                Pages.ref_point = self.ref_point.get()
                Pages.ref_dir = self.ref_dir.get()


            except ValueError:
                print("here")
                self.warning_text.set("Please make sure that the point and velocity are two numbers seperated by a comma")
                self.entryFlag = False




    def open_next_frame(self):
        """This function first calls the record params function to make sure everything is ok. If the option is manual, page two will be opened,
        if the option is CSV page three will be opened. If there is a mistake in the user input, the user will be informed"""
        self.record_params()
        print(self.entryFlag)

        if self.entryFlag == True and self.method == False:
            self.controller.show_frame("PageEleven")
        elif self.entryFlag == True and self.method == True:
            self.controller.show_frame("PageTwelve")
        else:
            self.warning_text.set("Please fill out the information correctly")


