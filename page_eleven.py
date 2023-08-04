import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter.filedialog import askopenfilename
import pandas as pd
from p import Pages
import re




class PageEleven(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller 

        self.flag1 = False 
        self.flag2 = False 
        self.flag3 = False  # New flag for the additional CSV/TXT file
        self.alpha_list = []; self.vector_list = []

        ttk.Label(self, text="Upload your CSV files please", font = ("bold", 20)).grid(row=1, column=0, padx = (10,30), pady = (10,30), columnspan=3)

        Btn_import1 = ttk.Button(self, text='Upload Positions', command=lambda:self.import_csv_data(1));  Btn_import1.grid(row=2, column=0, sticky='w')
        Btn_import2 = ttk.Button(self, text='Upload Directions', command=lambda:self.import_csv_data(2));  Btn_import2.grid(row=2, column=1, sticky='w')
        Btn_import3 = ttk.Button(self, text='Upload Energy', command=lambda:self.import_csv_data(3));  Btn_import3.grid(row=2, column=2, sticky='w')  # New button for the additional CSV/TXT file
        Btn_ok = ttk.Button(self, text='OK', command=lambda:self.open_window());  Btn_ok.grid(row=3, column=0, sticky='w')
        Btn_back = ttk.Button(self, text="Back", command=lambda: controller.show_frame("PageTen")); Btn_back.grid(row=3, column=1, sticky='w')

        self.path1 = StringVar(self, value=' ')
        self.text1 = ttk.Label(self, textvariable = self.path1).grid(row=4, column=0, columnspan=5, pady = 5)
        self.path2 = StringVar(self, value=' ')
        self.text2 = ttk.Label(self, textvariable = self.path2).grid(row=5, column=0, columnspan=5, pady = 5)
        self.path3 = StringVar(self, value=' ')  # New path variable for the additional CSV/TXT file
        self.text3 = ttk.Label(self, textvariable = self.path3).grid(row=6, column=0, columnspan=5, pady = 5)  # New label for the additional CSV/TXT file

    def import_csv_data(self, csv_number):
        csv_file_path = askopenfilename() 

        if csv_number == 1:
            path = self.path1
        elif csv_number == 2:
            path = self.path2
        elif csv_number == 3:  # New condition for the additional CSV/TXT file
            path = self.path3

        path.set(csv_file_path)

        if "csv" not in csv_file_path and "txt" not in csv_file_path: 
            path.set("Please input a CSV or TXT file only")
            if csv_number == 1:
                self.flag1 = False 
            elif csv_number == 2:
                self.flag2 = False 
            elif csv_number == 3:  # New condition for the additional CSV/TXT file
                self.flag3 = False

        else:
            path.set(csv_file_path)
            if csv_number == 1:
                self.flag1 = True 
            elif csv_number == 2:
                self.flag2 = True 
            elif csv_number == 3:  # New condition for the additional CSV/TXT file
                self.flag3 = True 

            df = pd.read_csv(csv_file_path) 

            # Read only the first row from the CSV and get the column names
            header_row = pd.read_csv(csv_file_path, nrows=1).columns
            # Check each column name for digits and return False if any are found
            is_header = all(not bool(re.search(r'\d', header)) for header in header_row)

            data = []
            if is_header:
                for _, row in df.iterrows():
                    data.append(row.tolist())
            else:
                df = pd.read_csv(csv_file_path, header=None) 
                for _, row in df.iterrows():
                    data.append(row.tolist())

            if csv_number == 1:
                Pages.pos_vector = data
            elif csv_number == 2:
                Pages.dir_vector = data
            elif csv_number == 3:  # New condition for the additional CSV/TXT file
                Pages.ener_vector = data  # Update this to the variable you want to use for the additional data

 

    def open_window(self):
        if self.flag1 and self.flag2: 
            self.controller.show_frame("PageTwelve")

        else:
            if not self.flag1:
                self.path1.set("Please upload a CSV or TXT file for the positions of the particles")
            if not self.flag2:
                self.path2.set("Please upload a CSV or TXT file for the directions of the particles")
            if not self.flag3:
                self.path3.set("Please upload a CSV or TXT file for the energies of the particles")

