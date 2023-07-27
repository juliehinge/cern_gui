import tkinter as tk
from tkinter import font as tkfont
from tkinter import ttk
from tkinter import *
from tkinter.filedialog import askopenfilename
import pandas as pd
from p import Pages

class PageThree(tk.Frame, Pages):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller # Initializing

        self.flag = False 
        self.alpha_list = []; self.vector_list = [] # This is for getting the angles and vector from the csv file

        ttk.Label(self, text="Upload your CSV file please", font = ("bold", 20)).grid(row=1, column=0, padx = (10,30), pady = (10,30), columnspan=3)
                
        # Making the buttons and placing them on the grid
        Btn_import = ttk.Button(self, text='Browse Data Set', command=lambda:self.import_csv_data());  Btn_import.grid(row=2, column=0, sticky='w')
        Btn_ok = ttk.Button(self, text='OK', command=lambda:self.open_window());  Btn_ok.grid(row=2, column=1, sticky='w')
        Btn_back = ttk.Button(self, text="Back", command=lambda: controller.show_frame("PageOne")); Btn_back.grid(row=2, column=2, sticky='w')

        # Warning text set up/Writing the path to the file that the user uploads
        self.path = StringVar(self, value=' '); self.text = ttk.Label(self, textvariable = self.path, foreground="red").grid(row=3, column=0, columnspan=3, pady = 5)


    def import_csv_data(self):

        csv_file_path = askopenfilename() # This allows the user to open their folder
        self.path.set(csv_file_path) 

        if "csv" not in csv_file_path: # Making sure the user only uploads a csv file
            self.path = StringVar(self, value="Please input a CSV file only") # Warning the user
            self.text = ttk.Label(self, textvariable = self.path,foreground ="red").grid(row=4, column=0, columnspan=3, pady = 5)
            self.flag = False # Setting the user mistake flag to False since the user didn't input the correct information

    
        else:
            self.path = StringVar(self, value=csv_file_path) # Writing the path of the file
            self.text = ttk.Label(self, textvariable = self.path).grid(row=4, column=0, columnspan=3, pady = 5)
            self.flag = True # The user didn't make a mistake so the flag is true

        
            self.path.set(csv_file_path)    # Writing the path of the file
            df = pd.read_csv(csv_file_path) # Reading in the csv as a pandas dataframe

            is_header = any(char.isdigit() for char in df) # Checking it there is a heading in the csv file

            if is_header:
                alpha = df.iloc[:, 0].tolist()
                vector = df.iloc[:, 1:].values.tolist() # Sa

            else:
                df = pd.read_csv(csv_file_path, header=None) 
                alpha = df.iloc[:, 0].tolist()
                vector = df.iloc[:, 1:].values.tolist()

            Pages.alpha_list = alpha
            Pages.vector_list = vector



    def open_window(self):
        if self.flag: # Only open the next window if there is no user mistake
            self.controller.show_frame("PageFour")

        else:
            self.path = StringVar(self, value="Please upload a CSV file") # Warning the user
            self.text = ttk.Label(self, textvariable = self.path,foreground ="red").grid(row=4, column=0, columnspan=3, pady = 5)
           


if __name__ == "__main__":
    app = PageThree()
    app.mainloop()
