import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkscrolledframe import ScrolledFrame
import random
from p import Pages


class PageTwo(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller # Initializing

        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)

        # Create the scrollable frame and display it
        self.sf = ScrolledFrame(self.container, width=640, height=400, scrollbars="vertical")
        self.sf.pack(fill="both", expand=True)
        self.scrollable_frame = self.sf.display_widget(tk.Frame)

        # Making labels and putting them on the frame
        label = tk.Label(self.scrollable_frame, text="Input information about the vectors please", font=("bold", 20))
        label.grid(row=0, column=0, padx=(10, 30), pady=(10, 20), sticky='w', columnspan=4)

        ttk.Label(self.scrollable_frame, text="-" * 100, foreground="grey").grid(row=1, column=0, pady=(10, 0),
                                                                                      columnspan=4, sticky='w')
      
        # Counters for row number and number of sections to keep track of them
        self.row = 1; self.counter = 0  
        self.alpha_entries = []; self.vector_entries = []; self.labels = [] # Lists to keep track of all the widgets

        # Putting the first section on the frame
        self.add_section()
        self.theme = ""
        self.is_dark_theme()

        # Create the frame at the bottom to contain all the buttons so they don't get in the way
        self.bottom_frame = tk.Frame(self.container)
        self.bottom_frame.pack(side="bottom")

        self.btn_add = ttk.Button(self.bottom_frame, text="Add Section", command=self.add_section)
        self.btn_add.grid(row=0, column=0, padx=(0,5), pady=5, sticky='w')

        self.btn_remove = ttk.Button(self.bottom_frame, text="Remove Section", command=self.remove_section)
        self.btn_remove.grid(row=0, column=1, padx=5, pady=5, sticky='w')

        self.btn_clear = ttk.Button(self.bottom_frame, text="Clear All", command=self.clear_all)
        self.btn_clear.grid(row=0, column=2, padx=5, pady=5, sticky='w')

        self.btn_ok = ttk.Button(self.bottom_frame, text="OK", width=5, command=self.sum_alpha)
        self.btn_ok.grid(row=1, column=1, pady=5, sticky='w')

        self.btn_back = ttk.Button(self.bottom_frame, text="Back",
                            command=lambda: controller.show_frame("PageOne"))
        self.btn_back.grid(row=1, column=0, pady=5, sticky='w')

        # Warning text set up
        self.warning_text = StringVar(self.bottom_frame, value=' ')
        self.text = ttk.Label(self.bottom_frame, textvariable=self.warning_text, foreground="red")
        self.text.grid(row=2, column=0, columnspan=5, padx=5, pady=(0,10))


 
    def is_dark_theme(self):
        """The function tests wether the user has a dark or light theme which is nessecarry when i change the colors from grey to black/white depending on the theme"""
        bg_color = self.cget("background")
        r, g, b = self.winfo_rgb(bg_color)
        average = (r + g + b) / (3 * 256)  # winfo_rgb returns in range 0-65535
        dark_theme = average < 128  # this threshold can be adjusted
    
        if dark_theme:
            self.theme = "dark"
        else:
            self.theme = "light"



    def add_section(self):

        i = self.row
        self.vector_section(i) # Calling the function that puts the vector on the gui
        self.alpha_section(i)# Calling the function that puts the alpha section on the gui
        lab = ttk.Label(self.scrollable_frame, text="-" * 100, foreground="grey")
        lab.grid(row=i + 3, column=0, pady=(10, 0), columnspan=5, sticky='w')
        self.labels.append(lab) # We append all labels to a list so we can delete them if the user wants to
        self.row += 3    # Increasing the row count with three since we just added three rows to the screen
        self.counter += 1   # Increasing the counter with 1 since we just added a section


    def vector_section(self, i):
        lab1 = ttk.Label(self.scrollable_frame, text=f"Section {self.counter + 1}", font=("bold", 15)) # Heading
        lab1.grid(row=self.row + 1, column=0, pady=(0, 10), sticky='w', columnspan=4)
        lab2 = ttk.Label(self.scrollable_frame, text='Bn:') # Bn label
        lab2.grid(row=self.row + 2, column=0, sticky='e')
        self.labels.append(lab1)  # We append all labels to a list so we can delete them if the user wants to
        self.labels.append(lab2)

        sections_entry = ttk.Entry(self.scrollable_frame, foreground="grey") # Putting the entry on the gui
        sections_entry.grid(row=self.row + 2, column=1, sticky='w')
        random_num = round(random.uniform(0,10), 1) # Placing a random number as placeholder in the entry
        sections_entry.insert(0, random_num)
        sections_entry.insert(3, ",")
        sections_entry.insert(4, round(random.uniform(0,10), 1))

        sections_entry.bind('<FocusIn>', lambda event: self.clear(event, sections_entry, random_num))

        self.vector_entries.append(sections_entry)
        
        lab3 = tk.Label(self.scrollable_frame, text="α (radians):", font=(10))
        lab3.grid(row=self.row + 2, column=2, sticky='e', padx=(10, 0))
        self.labels.append(lab3)



    def alpha_section(self, i):
        sections_entry = ttk.Entry(self.scrollable_frame, foreground="grey") # Putting the entry on the gui
        sections_entry.grid(row=self.row + 2, column=3, sticky='w')
        random_num = round(random.uniform(0,10), 1)  # Placing a random number as placeholder in the entry
        sections_entry.insert(0, random_num)
        sections_entry.bind('<FocusIn>', lambda event: self.clear(event, sections_entry, random_num))

        self.alpha_entries.append(sections_entry)


   

    def clear(self, event, sections_entry, random_num):


        """This function clears the number already in the entry"""
        if sections_entry.get() != '': # If the section is empty, there is nothing to clear
            try:
                entry_num = sections_entry.get().split(',')
                if float(entry_num[0]) == float(random_num): # We don't want to clear anything the user put in, just the random pre-placed numbers
                    sections_entry.delete(0, tk.END) # Deleting text already in box
                    if self.theme == "dark":
                        sections_entry.config(foreground="white") # Changing colour of the box
                    else:
                        sections_entry.config(foreground="black") # Changing colour of the box

            except AttributeError:
                if float(sections_entry.get()) == float(random_num): # We don't want to clear anything the user put in, just the random pre-placed numbers
                    sections_entry.delete(0, tk.END) # Deleting text already in box
                    if self.theme == "dark":
                            sections_entry.config(foreground="white") # Changing colour of the box
                    else:
                        sections_entry.config(foreground="black") # Changing colour of the box










    def remove_section(self):
        """Funtion to delete a section"""
        if self.counter > 1: # We don't want to clear the first section
            for i in self.labels[-5:-1]: # Loop through the labels that correspond to the last section and delete them from the list.
                i.destroy()
                self.labels.remove(i)

             # Destroy the last alpha and vector entry and delete them from the list.
            self.alpha_entries[-1].destroy() 
            self.alpha_entries.pop()

            self.vector_entries[-1].destroy()
            self.vector_entries.pop()
            self.counter -= 1 # Decrease the sections counter since we just deleted a section



    def clear_all(self):
        """This function clears all entries except for the first on"""
        for i in range(self.counter-1):
            self.remove_section()

    

    def sum_alpha(self):
        """This function is to make sure alpha doesn't exceed 360 degrees and to make sure there are no user mistakes in general"""
        alpha_sum = 0 # Counter to keep track of the current sum of degrees
        user_mistake = False # Flag to keep track of mistakes in the input

        updated_alpha = [] 
        updated_vector = []

        for i in self.vector_entries: 
            vector = i.get() # Getting the values of all vector entries and appending them to an updated version
            try:
                parts = vector.split(',')
                float_parts = [float(part) for part in parts]
                updated_vector.append(float_parts)
            except ValueError:
                self.warning_text.set("There is an error in one of your inputs!") # Warning the user
                user_mistake = True # Setting the flag to true since there is a mistake in the input
    

        # Looping through the buttons and getting their alpha value 
        for i in self.alpha_entries:
            alpha = i.get()
            try:
                alpha = float(alpha)
                alpha_sum += float(alpha) # adding to the alpha sum
                updated_alpha.append(alpha)
            except ValueError:
                self.warning_text.set("There is an error in one of your inputs!") # Warning the user
                user_mistake = True # Setting the flag to true since there is a mistake in the input
    
                            
        if alpha_sum > 360:
            self.warning_text.set("The total degrees should not exceed 360 degrees!") # Warning the user if the degrees exceed 360
    
        elif user_mistake == False:
            self.warning_text.set(" ") # Removing the warning if error is fixed
            Pages.alpha_list = updated_alpha # Passing the variables to the pages module
            Pages.vector_list = updated_vector
            self.controller.show_frame("Options") # Opening the next page
        
