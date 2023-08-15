import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkscrolledframe import ScrolledFrame
import random
from p import Pages


class PageTen(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller # Initializing

        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)

        # Create the scrollable frame and display it
        self.sf = ScrolledFrame(self.container, width=640, height=400, scrollbars="vertical")
        self.sf.pack(fill="both", expand=True)
        #self.sf.bind_arrow_keys(self.container); self.sf.bind_scroll_wheel(self.container)
        self.scrollable_frame = self.sf.display_widget(tk.Frame)

        # Making labels and putting them on the frame
        label = tk.Label(self.scrollable_frame, text="Input vectors of particle start positions and directions please ", font=("bold", 20))
        label.grid(row=0, column=0, padx=(10, 30), pady=(10, 20), sticky='w', columnspan=6)

        ttk.Label(self.scrollable_frame, text="-" * 150, foreground="grey").grid(row=1, column=0, pady=(10, 0),
                                                                                      columnspan=6, sticky='w')
      
        # Counters for row number and number of sections to keep track of them
        self.row = 1; self.counter = 0  
        self.part_point = []; self.part_dir = []; self.energy = []; self.labels = [] # Lists to keep track of all the widgets

        # Putting the first section on the frame
        self.add_section()

        # Create the frame at the bottom to contain all the buttons so they don't get in the way
        self.bottom_frame = tk.Frame(self.container)
        self.bottom_frame.pack(side="bottom")

        self.btn_add = ttk.Button(self.bottom_frame, text="Add Section", command=self.add_section)
        self.btn_add.grid(row=0, column=0, padx=5, pady=5)

        self.btn_remove = ttk.Button(self.bottom_frame, text="Remove Section", command=self.remove_section)
        self.btn_remove.grid(row=0, column=1, padx=5, pady=5)

        self.btn_clear = ttk.Button(self.bottom_frame, text="Clear All", command=self.clear_all)
        self.btn_clear.grid(row=0, column=2, padx=5, pady=5)

        self.btn_ok = ttk.Button(self.bottom_frame, text="OK", width=5, command=self.next_frame)
        self.btn_ok.grid(row=1, column=1, pady=5)

        self.btn_back = ttk.Button(self.bottom_frame, text="Back",
                            command=lambda: self.go_back())
        self.btn_back.grid(row=1, column=0, pady=5)

        # Warning text set up
        self.warning_text = StringVar(self.bottom_frame, value=' ')
        self.text = ttk.Label(self.bottom_frame, textvariable=self.warning_text, foreground="red")
        self.text.grid(row=2, column=0, columnspan=6, padx=5, pady=5)




    def add_section(self):
        i = self.row
        self.point_section(i)# Calling the function that puts the direction section on the gui
        self.dir_section(i)# Calling the function that puts the direction section on the gui
        self.energy_section(i)
        lab = ttk.Label(self.scrollable_frame, text="-" * 150, foreground="grey")
        lab.grid(row=i + 3, column=0, pady=(10, 0), columnspan=6, sticky='w')
        self.labels.append(lab) # We append all labels to a list so we can delete them if the user wants to
        self.row += 3    # Increasing the row count with three since we just added three rows to the screen
        self.counter += 1   # Increasing the counter with 1 since we just added a section





    def point_section(self, i):
        lab1 = ttk.Label(self.scrollable_frame, text=f"Particle {self.counter + 1}", font=("bold", 15)) # Heading
        lab1.grid(row=self.row + 1, column=0, pady=(0, 10), sticky='w', columnspan=6)

        lab2 = ttk.Label(self.scrollable_frame, text='Position:') # position label
        lab2.grid(row=self.row + 2, column=0, sticky='e')
        self.labels.append(lab1)  # We append all labels to a list so we can delete them if the user wants to
        self.labels.append(lab2)


        sections_entry = ttk.Entry(self.scrollable_frame, foreground="grey") # Putting the entry on the gui
        sections_entry.grid(row=self.row + 2, column=1, sticky='w')
        random_num = round(random.uniform(0,10), 1)  # Placing a random number as placeholder in the entry
        random_num2 = round(random.uniform(0,10), 1)
        sections_entry.insert(0, random_num)
        sections_entry.insert(3, ",")
        sections_entry.insert(4, random_num2)
        sections_entry.bind('<FocusIn>', lambda event: self.clear(event, sections_entry, random_num))
        self.part_point.append(sections_entry)






    def dir_section(self, i):
        lab2 = ttk.Label(self.scrollable_frame, text='Direction:') # direction label
        lab2.grid(row=self.row + 2, column=2, sticky='e')
        self.labels.append(lab2)
        sections_entry = ttk.Entry(self.scrollable_frame, foreground="grey") # Putting the entry on the gui
        sections_entry.grid(row=self.row + 2, column=3, sticky='w')
        random_num = round(random.uniform(0,10), 1)  # Placing a random number as placeholder in the entry
        random_num2 = round(random.uniform(0,10), 1)

        sections_entry.insert(0, random_num)
        sections_entry.insert(3, ",")
        sections_entry.insert(4, random_num2)
        sections_entry.bind('<FocusIn>', lambda event: self.clear(event, sections_entry, random_num))

        self.part_dir.append(sections_entry)




    def energy_section(self, i):
        lab2 = ttk.Label(self.scrollable_frame, text='Energy:') # direction label
        lab2.grid(row=self.row + 2, column=4, sticky='e')
        self.labels.append(lab2)
        sections_entry = ttk.Entry(self.scrollable_frame, foreground="grey") # Putting the entry on the gui
        sections_entry.grid(row=self.row + 2, column=5, sticky='w')
        random_num = random.randrange(100, 200, 5) # Placing a random number as placeholder in the entry
        sections_entry.insert(0, random_num)

        sections_entry.bind('<FocusIn>', lambda event: self.clear(event, sections_entry, random_num))
        self.energy.append(sections_entry)




    def clear(self, event, sections_entry, random_num):

        """This function clears the number already in the entry"""
        if sections_entry.get() != '': # If the section is empty, there is nothing to clear
            try:
                entry_num = sections_entry.get().split(',')
                if float(entry_num[0]) == float(random_num): # We don't want to clear anything the user put in, just the random pre-placed numbers
                    sections_entry.delete(0, tk.END) # Deleting text already in box
                    sections_entry.config(foreground="white") # Changing colour of the box
            except AttributeError:
                if float(sections_entry.get()) == float(random_num): # We don't want to clear anything the user put in, just the random pre-placed numbers
                    sections_entry.delete(0, tk.END) # Deleting text already in box
                    sections_entry.config(foreground="white") # Changing colour of the box





    def remove_section(self):
        """Funtion to delete a section"""
        if self.counter > 1: # We don't want to clear the first section
            for i in self.labels[-5:-1]: # Loop through the labels that correspond to the last section and delete them from the list.
                i.destroy()
                self.labels.remove(i)

             # Destroy the last direction and vector entry and delete them from the list.
            self.part_dir[-1].destroy() 
            self.part_dir.pop()
            self.part_point[-1].destroy() 
            self.part_point.pop()
            self.energy[-1].destroy() 
            self.energy.pop()
            self.counter -= 1 # Decrease the sections counter since we just deleted a section







    def clear_all(self):
        """This function clears all entries except for the first on"""
        for i in self.labels[4:]: # We dont include the first section which is why we start from three in the loop
            i.destroy()

        for i, j,k in zip(self.part_point[1:], self.part_dir[1:], self.energy[1:]):
            j.destroy()
            i.destroy()
            k.destroy()
            self.counter -= 1 # Decrease sections counter each time we delete a section

        ttk.Label(self.scrollable_frame, text="-" * 150, foreground="grey").grid(row=self.row, column=0, pady=(10, 0),
                                                                                  columnspan=6, sticky='w')



    def next_frame(self):


        user_mistake = False # Flag to keep track of mistakes in the input

        updated_point = []
        updated_dir = []
        updated_energy = []

        for i in self.part_point:
            i = i.get()
            try:
                parts = i.split(',')
                # There should be exactly 2 parts
                if len(parts) != 2:
                    user_mistake = True
                # Both parts should be convertible to a float 
    
                self.warning_text.set("")
                user_mistake = False
                updated_point.append(i)

            except ValueError:
                self.warning_text.set("Please make sure that the initial position of the particle is two coordinates seperated by a comma")
                user_mistake = True


        for i in self.part_dir:
            i = i.get()
            try:
                parts = i.split(',')
                # There should be exactly 2 parts
                if len(parts) != 2:
                    user_mistake = True
                # Both parts should be convertible to a float 
    
                self.warning_text.set("")
                user_mistake = False
                updated_dir.append(i)

            except ValueError:
                self.warning_text.set("Please make sure that the direction of the particle is two coordinates seperated by a comma")
                user_mistake = True





        for i in self.energy:
            i = i.get()
            try:
                float(i) # The energy shouldn't be a string

                self.warning_text.set("")
                user_mistake = False
                updated_energy.append(i)

            except ValueError:
                self.warning_text.set("Please make sure that the energy of all particles is a proper number")
                user_mistake = True


        if user_mistake == False:
            self.warning_text.set(" ") # Removing the warning if error is fixed
            Pages.dir_vector = updated_dir
            Pages.pos_vector = updated_point
            Pages.ener_vector = updated_energy

            
            if Pages.open_optimization == False:
                self.controller.show_frame("PageFourteen") # Opening the next page
            else:
                self.controller.show_frame("PageSixteen")

    def go_back(self):

        if Pages.manual == True:
            self.controller.show_frame("PageEight")
        else:
            self.controller.show_frame("PageEleven")