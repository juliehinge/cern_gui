import tkinter as tk
#from tkinter import font as tkfont
from tkinter import ttk
from p import Pages

class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller # Initialising

        # Adding labels to the GUI and placing them on the grid
        tk.Label(self, text="Input your magnet parameters please", font = ("bold", 20)).grid(row=0, column=0, padx = (10), pady = (10), columnspan=2)
        ttk.Label(self, text="-"*80, foreground="grey").grid(row=1, column=0, pady = (10,0), columnspan = 5, sticky='w')
        tk.Label(self, text="Reference Radius:", font = ("bold", 15)).grid(row=2, column=0, pady=10, sticky='w', )
        tk.Label(self, text="Input Sections:", font = ("bold", 15)).grid(row=4, column=0,pady=(10,0), sticky='w')
        ttk.Label(self, text="-"*80, foreground="grey").grid(row=3, column=0, pady = (10,0), columnspan = 5, sticky='w')
        ttk.Label(self, text="-"*80, foreground="grey").grid(row=6, column=0, pady = (10,0), columnspan = 5, sticky='w')

        # Adding an entry for the radius so the user can input it.
        self.r_radius_entry = ttk.Entry(self)
        self.r_radius_entry.grid(row=2, column=1, padx=2, sticky = 'w')

        # This is the setup for the checkboxes
        self.var1 = tk.IntVar()
        self.var2 = tk.IntVar()
        c1 = tk.Checkbutton(self, text='Manual',variable=self.var1, onvalue=1, offvalue=0, command=self.get_selection)
        c1.grid(row=4, column=1, pady=(10,0), sticky='w')
        c2 = tk.Checkbutton(self, text='By CSV upload',variable=self.var2, onvalue=1, offvalue=0, command=self.get_selection)
        c2.grid(row=5, column=1, sticky='w', pady=(0,10))

        
        # Making a backbutton and ok button and placing them on the grid
        button1 = ttk.Button(self, text="Back",
                            command=lambda: controller.show_frame("StartPage"))
        button1.grid(row=7, column=0,  pady = (10), sticky='e')


        button2 = ttk.Button(self, text="OK",
                            command=lambda: self.open_next_frame())
        button2.grid(row=7, column=1,  pady = (10), sticky='w')



        # Warning text setup
        self.warning_text = tk.StringVar(self, value=' ')
        self.text = ttk.Label(self, textvariable = self.warning_text, foreground ="red").grid(row=10, column=0,pady = 5, columnspan=3)
        

        # Flags for confirming that the user input is correct
        self.checkFlag = False
        self.entryFlag = False
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
        radius = self.r_radius_entry.get() # Getting the radius from the entrybox
        # Ensuring the radius is an integer
        if radius.replace(".", "").isnumeric()== False:
            self.entryFlag = False
        # Ensuring the radius is larger than 0
        elif float(radius) < 0:
                self.entryFlag = False
        # When error is fixed, the text disappears and the new window is opened
        else:
            self.warning_text.set("") 
            self.entryFlag = True # Now that there is no user mistake we can set the flag to true
            Pages.radius = float(radius) # We set the radius on the Pages module so we can pass it forward to other windows


    def open_next_frame(self):
        """This function first calls the record params function to make sure everything is ok. If the option is manual, page two will be opened,
        if the option is CSV page three will be opened. If there is a mistake in the user input, the user will be informed"""
        self.record_params()
        if self.checkFlag == True and self.entryFlag == True and self.method == False:
            self.controller.show_frame("PageTwo")
        elif self.checkFlag == True and self.entryFlag == True and self.method == True:
            self.controller.show_frame("PageThree")
        else:
            self.warning_text.set("Please fill out the information correctly")


