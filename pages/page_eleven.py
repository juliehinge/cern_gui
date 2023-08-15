import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilenames
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




        ttk.Label(self, text="Upload your CSV files please", font = ("bold", 20)).grid(row=0, column=0, padx = (10,30), pady = (10,30), columnspan=3)
        ttk.Label(self, text="-"*100, foreground="grey").grid(row=1, column=0, pady = (10,0), columnspan = 5, sticky='w')

        tk.Label(self, text="Tracking size (m)").grid(row=2, column=0, pady=10, sticky='e')
        self.track = ttk.Entry(self, width=5); self.track.grid(row=2, column=1, pady=10, sticky='w', )




        ttk.Label(self, text="Enter the number beams you want displayed:", font=("bold", 10)).grid(row=4, column=0, padx=10, pady=10)
        self.num_files = tk.IntVar(value=0)
        ttk.Entry(self, textvariable=self.num_files).grid(row=4, column=1, padx=10, pady=10)
        ttk.Button(self, text='Set', command=self.set_num_files).grid(row=4, column=2, sticky='w')

        self.back_button = ttk.Button(self, text="Back", command=lambda: self.controller.show_frame("Options"))
        self.back_button.grid(row=4, column=3, sticky='w')  # Placing it next to the Set button

        self.upload_buttons = []
        self.delete_buttons = []
        self.ok_button = None
        #self.back_button = None
        self.warning = tk.StringVar(self, value=' ')
       
     


    def set_num_files(self):
        self.file_count = {category: 1 for category in ['Positions', 'Directions', 'Energies']}
        self.file_data = {}

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
            upload_button = ttk.Button(self, text=f'Upload {category} File', command=lambda category=category: self.import_csv_data(category))
            upload_button.grid(row=6+category_index, column=0, sticky='w')
            self.upload_buttons.append(upload_button)

            # Initialize with an empty string
            self.paths[category] = tk.StringVar(self, value='')
            ttk.Label(self, textvariable=self.paths[category]).grid(row=6+category_index, column=1, sticky='w')

            delete_button = ttk.Button(self, text=f'Delete Last {category} File', command=lambda category=category: self.delete_last_file(category))
            delete_button.grid(row=6+category_index, column=2, sticky='w')
            self.delete_buttons.append(delete_button)

        self.ok_button = ttk.Button(self, text='OK', command=self.open_window)
        self.ok_button.grid(row=10+category_index, column=0, sticky='w')
        self.back_button.grid(row=10+category_index, column=1, sticky='w')  # Adjust the row index if needed

        warning_label = ttk.Label(self, textvariable=self.warning)
        warning_label.grid(row=11+category_index, column=0, columnspan=5, pady=5)
        warning_label.config(foreground='red')




    def import_csv_data(self, category):
        selected_files = askopenfilenames()  # This returns a tuple of selected file paths

        # If no files were selected, exit the function
        if not selected_files:
            return

        existing_paths = [path for path in self.paths[category].get().split(', ') if path]

        for csv_file in selected_files:

            if "csv" not in csv_file and "txt" not in csv_file: 
                self.flags[category] = False
                continue

            df = pd.read_csv(csv_file) 
            header_row = pd.read_csv(csv_file, nrows=1).columns
            is_header = all(not bool(re.search(r'\d', header)) for header in header_row)

            data = []
            if is_header:
                for _, row in df.iterrows():
                    data.append(row.tolist())
            else:
                df = pd.read_csv(csv_file, header=None) 
                for _, row in df.iterrows():
                    data.append(row.tolist())

            self.file_count[category] += 1
            file_key = f"file{self.file_count[category]}"
            
            if category == 'Directions':
                existing_paths.append(f'dir{self.file_count[category]}')
            elif category == 'Positions':
                existing_paths.append(f'pos{self.file_count[category]}')
            elif category == 'Energies':
                existing_paths.append(f'ener{self.file_count[category]}')

            self.file_data[category] = self.file_data.get(category, {})
            self.file_data[category][file_key] = data
            self.flags[category] = True 

        self.paths[category].set(", ".join(existing_paths))

    def delete_last_file(self, category):
        if self.file_data[category]:
            last_file_key = list(self.file_data[category].keys())[-1]
            del self.file_data[category][last_file_key]
           # paths = self.paths[category].get().split(',')
            if category == 'Directions':
                self.paths[category].set(f'dir{self.file_count[category]-1}' if self.file_count[category] > 1 else '')
            elif category == 'Positions':
                self.paths[category].set(f'pos{self.file_count[category]-1}' if self.file_count[category] > 1 else '')
            elif category == 'Energies':
                self.paths[category].set(f'ener{self.file_count[category]-1}' if self.file_count[category] > 1 else '')
        
            #self.paths[category].set(','.join(paths))
            self.paths[category].set(f'dir{self.file_count[category]-1}')
            self.file_count[category] -= 1




    def open_window(self):
        if all(self.flags.values()): 
            lengths = []
            for category_dict in self.file_data.values():
                lengths.append([len(data) for data in category_dict.values()])

            # Transpose lengths for easy comparison
            lengths = list(map(list, zip(*lengths)))

            if all(len(set(lst)) == 1 for lst in lengths):
                Pages.file_data = self.file_data

                try:
                    float(self.track.get())
                    self.warning.set("")
                    Pages.tracking = float(self.track.get())
                    if Pages.open_optimization == False:
                        self.controller.show_frame("PageFourteen")
                    else:
                        self.controller.show_frame("PageFifteen")

                except TypeError:
                    self.warning.set("Please make sure the tracking size is a real number in meters")
            else:
                mismatched_files = []
                for i, lst in enumerate(lengths):
                    if len(set(lst)) != 1:
                        for j, length in enumerate(lst):
                            if length != lst[0]:
                                mismatched_files.append(f'file{i+1} in {list(self.file_data.keys())[j]}')
                self.warning.set("There is a length mismatch in the following files: " + ', '.join(mismatched_files))
        else:
            for category, flag in self.flags.items():
                if not flag:
                    self.paths[category].set(f"Please upload a CSV or TXT file for {category}")
