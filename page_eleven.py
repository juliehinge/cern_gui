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

        self.flags = {}
        self.paths = {} 
        self.file_data = {}

        ttk.Label(self, text="Upload your CSV files please", font = ("bold", 20)).grid(row=1, column=0, padx = (10,30), pady = (10,30), columnspan=3)

        ttk.Label(self, text="Enter the number of files you want to upload for each category:", font=("bold", 10)).grid(row=2, column=0, padx=10, pady=10)
        self.num_files = tk.IntVar(value=0)
        ttk.Entry(self, textvariable=self.num_files).grid(row=2, column=1, padx=10, pady=10)
        ttk.Button(self, text='Set', command=self.set_num_files).grid(row=2, column=2, sticky='w')

        self.upload_buttons = []
        self.ok_button = None
        self.back_button = None

    def set_num_files(self):
        for button in self.upload_buttons:
            button.grid_forget()
        if self.ok_button:
            self.ok_button.grid_forget()
        if self.back_button:
            self.back_button.grid_forget()

        categories = ['Positions', 'Directions', 'Energies']
        for category_index, category in enumerate(categories, start=1):
            button = ttk.Button(self, text=f'Upload {category} Files', command=lambda category=category: self.import_csv_data(category))
            button.grid(row=3+category_index, column=0, sticky='w')
            self.upload_buttons.append(button)

            self.paths[category] = StringVar(self, value=' ')
            ttk.Label(self, textvariable=self.paths[category]).grid(row=3+category_index, column=1, columnspan=5, pady=5)
            
            for i in range(self.num_files.get()):
                file_number = (category, i+1)  # using tuple (category, index) as the key
                self.flags[file_number] = False 

        self.ok_button = ttk.Button(self, text='OK', command=self.open_window)
        self.ok_button.grid(row=5+category_index, column=0, sticky='w')
        self.back_button = ttk.Button(self, text="Back", command=lambda: self.controller.show_frame("PageTen"))
        self.back_button.grid(row=5+category_index, column=1, sticky='w')

    def import_csv_data(self, category):
        csv_file_paths = askopenfilename(multiple=True)  # allows multiple file selection

        path_list = []
        for i, csv_file_path in enumerate(csv_file_paths):
            file_number = (category, i+1)  # using tuple (category, index) as the key
            path = self.paths.get(category)

            if not path:
                continue  # Skip if the file number doesn't exist (i.e., more files were selected than specified)

            path_list.append(csv_file_path[:5])  # Append the first 5 letters of the file path to the list
            
            if "csv" not in csv_file_path and "txt" not in csv_file_path: 
                self.flags[file_number] = False
            else:
                self.flags[file_number] = True 

                df = pd.read_csv(csv_file_path) 
                header_row = pd.read_csv(csv_file_path, nrows=1).columns
                is_header = all(not bool(re.search(r'\d', header)) for header in header_row)

                data = []
                if is_header:
                    for _, row in df.iterrows():
                        data.append(row.tolist())
                else:
                    df = pd.read_csv(csv_file_path, header=None) 
                    for _, row in df.iterrows():
                        data.append(row.tolist())

                self.file_data[file_number] = data

        self.paths[category].set(','.join(path_list))  # Set the variable to the joined string

    def open_window(self):
        if all(self.flags.values()): 
            Pages.file_data = self.file_data
            self.controller.show_frame("PageTwelve")
        else:
            for file_number, flag in self.flags.items():
                if not flag:
                    category, i = file_number
                    self.paths[category].set(f"Please upload a CSV or TXT file for {category} file {i}")
