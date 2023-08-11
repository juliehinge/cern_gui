import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkscrolledframe import ScrolledFrame
import random
from p import Pages

class PageTwelve(tk.Frame, Pages):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)

        # This is to pass the variables from the csv
        self.bind("<<ShowFrame>>", self.pasvariable)

        # Create the scrollable frame
        self.sf = ScrolledFrame(self.container, width=640, height=400, scrollbars="vertical")
        self.sf.pack(fill="both", expand=True)
        self.scrollable_frame = self.sf.display_widget(tk.Frame)

        label = tk.Label(self.scrollable_frame, text="This is the CSV section", font=("bold", 20))
        label.grid(row=0, column=0, padx=(10, 30), pady=(10, 20), sticky='w', columnspan=6)

        # Counters for row number and number of sections
        self.row = 1; self.counter = 1  
        self.dir_entries = []; self.pos_entries = [];self.energy_entries = []; self.labels = [] # Lists to keep track of all the widgets


       # Create the frame at the bottom
        self.bottom_frame = tk.Frame(self.container)
        self.bottom_frame.pack(side="bottom", fill="x")


        self.btn_add = ttk.Button(self.bottom_frame, text="Add Section", command=self.add_section)
        self.btn_add.grid(row=0, column=0, padx=5, pady=5)

        self.btn_remove = ttk.Button(self.bottom_frame, text="Remove Section", command=self.remove_section)
        self.btn_remove.grid(row=0, column=1, padx=5, pady=5)

        self.btn_clear = ttk.Button(self.bottom_frame, text="Clear All", command=self.clear_all)
        self.btn_clear.grid(row=0, column=2, padx=5, pady=5)

        self.btn_ok = ttk.Button(self.bottom_frame, text="OK", width=5, command=self.next_frame)
        self.btn_ok.grid(row=1, column=1, padx=5, pady=5)

        self.btn_back = ttk.Button(self.bottom_frame, text="Back",
                            command=self.go_back)
        self.btn_back.grid(row=1, column=0, padx=5, pady=5)



        self.warning_text = StringVar(self.bottom_frame, value=' ')
        self.text = ttk.Label(self.bottom_frame, textvariable=self.warning_text, foreground="red")
        self.text.grid(row=2, column=0, columnspan=5, padx=5, pady=5)


    def pasvariable(self, var):
      
        if len(self.dir_entries) == 0:
            dir_list = Pages.dir_vector
            pos_list = Pages.pos_vector
            energy_list = Pages.ener_vector

            i = 0
            while i < len(dir_list) and i < 100:
                self.dir = dir_list[i]
                self.pos = pos_list[i]
                self.energy = energy_list[i]
                self.automatic_add() # Calling the function to actually add direction and the position of the particle
                i += 1



    def automatic_add(self):
        # Adding Labels For position
        sec_ent = ttk.Label(self.scrollable_frame, text=f"Particle {self.counter}", font = ("bold", 15)); sec_ent.grid(row=self.row+1, column=0, padx=(5,0), pady = (0,10), sticky='w')
        Bn_lab = ttk.Label(self.scrollable_frame, text='Position')
        Bn_lab.grid(row=self.row+2, column=0,  padx=(5,0), sticky='e')
        self.labels.append(sec_ent); self.labels.append(Bn_lab)
        
        # Adding Entries for position of particle
        sections_entry = ttk.Entry(self.scrollable_frame); sections_entry.grid(row=self.row+2, column=1, sticky = 'w')
        pos = ' '.join([str(elem) for elem in self.pos])
        pos = pos.replace(" ", ", ")
        sections_entry.insert(0, pos)
        self.pos_entries.append(sections_entry)

        # Adding Labels For direction of particle
        alp_lab = ttk.Label(self.scrollable_frame, text="Direction:")
        alp_lab.grid(row=self.row+2, column=2, sticky='e')
        self.labels.append(alp_lab)

        # Adding entries for direction of particle
        dir_entry = ttk.Entry(self.scrollable_frame); dir_entry.grid(row=self.row+2, column=3, sticky = 'w')
        dir = ' '.join([str(elem) for elem in self.dir])
        dir = dir.replace(" ", ", ")
        dir_entry.insert(0, dir)
        self.dir_entries.append(dir_entry)



        # Adding Labels For energy of particle
        alp_lab = ttk.Label(self.scrollable_frame, text="Energy:")
        alp_lab.grid(row=self.row+2, column=4, sticky='e')
        self.labels.append(alp_lab)



        # Adding entries for energies of particles
        energy_entry = ttk.Entry(self.scrollable_frame); energy_entry.grid(row=self.row+2, column=5, sticky = 'w')
        energy = float(self.energy[0])
        energy_entry.insert(0, energy)
        self.energy_entries.append(energy_entry)


        lab = ttk.Label(self.scrollable_frame, text="-"*150, foreground="grey")
        lab.grid(row=self.row+3, column=0, pady = (10,0), columnspan = 6, sticky='w')
        self.labels.append(lab) # Apending to list of labels
        self.row += 3; self.counter += 1 # Increment row number for new section and Increment the number of sections



 
    def add_section(self):

        # Adding Labels For positions of the particle
        sec_ent = ttk.Label(self.scrollable_frame, text=f"Section {self.counter}", font = ("bold", 15)); sec_ent.grid(row=self.row+1, column=0, padx=(5,0), pady = (0,10), sticky='w')
        Bn_lab = ttk.Label(self.scrollable_frame, text='Bn')
        Bn_lab.grid(row=self.row+2, column=0,  padx=(5,0), sticky='e')
        self.labels.append(sec_ent); self.labels.append(Bn_lab)

        # Adding Entries for position of particle
        sections_entry_v = ttk.Entry(self.scrollable_frame, foreground="grey"); sections_entry_v.grid(row=self.row+2, column=1, sticky = 'w')
        random_num_v = round(random.uniform(0,10), 1)
        sections_entry_v.insert(0, random_num_v)
        sections_entry_v.bind("<FocusIn>", lambda event: self.clear(event, sections_entry_v, random_num_v),) # Binding to an event to clear text already in box
        self.pos_entries.append(sections_entry_v)

        # Adding Labels For the direction of the particle
        alpha_lab = ttk.Label(self.scrollable_frame, text="Direction:")
        alpha_lab.grid(row=self.row+2, column=2, sticky='e')
        self.labels.append(alpha_lab)


        # Adding Entries for direction of particle
        sections_entry_a = ttk.Entry(self.scrollable_frame, foreground="grey"); sections_entry_a.grid(row=self.row+2, column=3, sticky = 'w')
        random_num = round(random.uniform(0,10), 1)
        sections_entry_a.insert(0, random_num)
        sections_entry_a.bind("<FocusIn>", lambda event: self.clear(event, sections_entry_a, random_num),) # Binding to an event to clear text already in box
        self.dir_entries.append(sections_entry_a)



        # Adding Labels For the energy of the particle
        energy_lab = ttk.Label(self.scrollable_frame, text="Energy:")
        energy_lab.grid(row=self.row+2, column=4, sticky='e')
        self.labels.append(energy_lab)


        # Adding Entries for engergy of particle
        sections_entry_energy = ttk.Entry(self.scrollable_frame, foreground="grey"); sections_entry_energy.grid(row=self.row+2, column=5, sticky = 'w')
        random_num = random.randrange(100, 200, 5) # Placing a random number as placeholder in the entry
        sections_entry_energy.insert(0, random_num)

        sections_entry_energy.bind("<FocusIn>", lambda event: self.clear(event, sections_entry_energy, random_num),) # Binding to an event to clear text already in box
        self.energy_entries.append(sections_entry_energy)


        lab = ttk.Label(self.scrollable_frame, text="-"*150, foreground="grey")
        lab.grid(row=self.row+3, column=0, pady = (10,0), columnspan = 6, sticky='w')
        self.labels.append(lab) # Apending to list of labels
        self.row += 3; self.counter += 1 # Increment row number for new section and Increment the number of sections

  




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
        if self.counter > 1: 
            for i in self.labels[-6:-1]:
                i.destroy()
                self.labels.remove(i)

            self.dir_entries[-1].destroy()
            self.dir_entries.pop()
            
            self.pos_entries[-1].destroy()
            self.pos_entries.pop()    

            self.energy_entries[-1].destroy()
            self.energy_entries.pop()   
            self.counter -= 1 # Decreasing the counter for every section we remove



    def clear_all(self):
        """This function clears all entries except for the first on"""
        for i in range(self.counter-1):
            self.remove_section()

    


    def next_frame(self):

        print("test")
        user_mistake = False # Flag to keep track of mistakes in the input

        updated_point = []
        updated_dir = []
        updated_energy = []


        for i in self.pos_entries:
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
                self.warning_text.set("Please make sure that the initial position of the particle two coordinates seperated by a comma")
                user_mistake = True


        for i in self.dir_entries:
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
                self.warning_text.set("Please make sure that the direction of the particle two coordinates seperated by a comma")
                user_mistake = True



        for i in self.energy_entries:
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
            print(Pages.open_optimization)
            print("test")
            if Pages.open_optimization == False:
                self.controller.show_frame("PageFourteen") # Opening the next page
            else:
                self.controller.show_frame("PageSixteen")
        

    def go_back(self):

        if Pages.manual == True:
            self.controller.show_frame("PageEight")

        else:
            self.controller.show_frame("PageEleven")
