import tkinter as tk
from tkinter import ttk
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
        self.delete_buttons = []
        self.ok_button = None
        self.back_button = None
        self.warning = tk.StringVar(self, value=' ')

    def set_num_files(self):
        for button in self.upload_buttons:
            button.grid_forget()
        for button in self.delete_buttons:
            button.grid_forget()
        if self.ok_button:
            self.ok_button.grid_forget()
        if self.back_button:
            self.back_button.grid_forget()

        categories = ['Positions', 'Directions', 'Energies']
        for category_index, category in enumerate(categories, start=1):
            upload_button = ttk.Button(self, text=f'Upload {category} Files', command=lambda category=category: self.import_csv_data(category))
            upload_button.grid(row=3+category_index, column=0, sticky='w')
            self.upload_buttons.append(upload_button)

            delete_button = ttk.Button(self, text=f'Delete Last {category} File', command=lambda category=category: self.delete_last_file(category))
            delete_button.grid(row=3+category_index, column=1, sticky='w')
            self.delete_buttons.append(delete_button)

            self.paths[category] = tk.StringVar(self, value=' ')
            ttk.Label(self, textvariable=self.paths[category]).grid(row=3+category_index, column=2, columnspan=5, pady=5)

        self.ok_button = ttk.Button(self, text='OK', command=self.open_window)
        self.ok_button.grid(row=6+category_index, column=0, sticky='w')
        self.back_button = ttk.Button(self, text="Back", command=lambda: self.controller.show_frame("PageTen"))
        self.back_button.grid(row=6+category_index, column=1, sticky='w')
        ttk.Label(self, textvariable=self.warning).grid(row=6+category_index, column=2, columnspan=5, pady=5)

    def import_csv_data(self, category):
        csv_file_path = askopenfilename()  # allows single file selection

        path = csv_file_path[:5]  # Get the first 5 letters of the file path

        if "csv" not in csv_file_path and "txt" not in csv_file_path: 
            self.flags[category] = False
        else:
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

            if category in self.file_data:
                self.file_data[category].append(data)
            else:
                self.file_data[category] = [data]

            self.flags[category] = True 
            # update existing path for the category with the new file path
            existing_path = self.paths[category].get()
            self.paths[category].set(existing_path + ',' + path if existing_path else path)

    def delete_last_file(self, category):
        if self.file_data[category]:
            self.file_data[category].pop()
            paths = self.paths[category].get().split(',')
            paths.pop()
            self.paths[category].set(','.join(paths))

    def open_window(self):
        if all(self.flags.values()): 
            lengths = []
            for data_list in self.file_data.values():
                lengths.append([len(data) for data in data_list])

            # Transpose lengths for easy comparison
            lengths = list(map(list, zip(*lengths)))

            if all(len(set(lst)) == 1 for lst in lengths):
                Pages.file_data = self.file_data
                self.controller.show_frame("PageTwelve")
            else:
                self.warning.set("Corresponding files in each category must have the same length.")
        else:
            for category, flag in self.flags.items():
                if not flag:
                    self.paths[category].set(f"Please upload a CSV or TXT file for {category}")
