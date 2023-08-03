import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkscrolledframe import ScrolledFrame
import random
from p import Pages

class PageFour(tk.Frame, Pages):
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
        label.grid(row=0, column=0, padx=(10, 30), pady=(10, 20), sticky='w', columnspan=4)

        # Counters for row number and number of sections
        self.row = 1; self.counter = 1  
        self.alpha_entries = []; self.vector_entries = []; self.labels = [] # Lists to keep track of all the widgets


       # Create the frame at the bottom
        self.bottom_frame = tk.Frame(self.container)
        self.bottom_frame.pack(side="bottom", fill="x")


        self.btn_add = ttk.Button(self.bottom_frame, text="Add Section", command=self.add_section)
        self.btn_add.grid(row=0, column=0, padx=5, pady=5)

        self.btn_remove = ttk.Button(self.bottom_frame, text="Remove Section", command=self.remove_section)
        self.btn_remove.grid(row=0, column=1, padx=5, pady=5)

        self.btn_clear = ttk.Button(self.bottom_frame, text="Clear All", command=self.clear_all)
        self.btn_clear.grid(row=0, column=2, padx=5, pady=5)

        self.btn_ok = ttk.Button(self.bottom_frame, text="OK", width=5, command=self.sum_alpha)
        self.btn_ok.grid(row=1, column=1, padx=5, pady=5)

        self.btn_back = ttk.Button(self.bottom_frame, text="Back",
                            command=lambda: controller.show_frame("PageThree"))
        self.btn_back.grid(row=1, column=0, padx=5, pady=5)



        self.warning_text = StringVar(self.bottom_frame, value=' ')
        self.text = ttk.Label(self.bottom_frame, textvariable=self.warning_text, foreground="red")
        self.text.grid(row=2, column=0, columnspan=5, padx=5, pady=5)


    def pasvariable(self, var):
      
        # Looping over the alpha list and vecor list from the csv and adding them to the entries 
        if len(self.alpha_entries) == 0:
            alpha_list = Pages.alpha_list
            vector_list = Pages.vector_list
            for i in range(len(alpha_list)):
                self.alpha = alpha_list[i]
                self.vector = vector_list[i]
                self.automatic_add() # Calling the function to actually add alpha and the vector




    def automatic_add(self):
        # Adding Labels For vector
        sec_ent = ttk.Label(self.scrollable_frame, text=f"Section {self.counter}", font = ("bold", 15)); sec_ent.grid(row=self.row+1, column=0, padx=(5,0), pady = (0,10), sticky='w')
        Bn_lab = ttk.Label(self.scrollable_frame, text='Bn')
        Bn_lab.grid(row=self.row+2, column=0,  padx=(5,0), sticky='e')
        self.labels.append(sec_ent); self.labels.append(Bn_lab)
        
        # Adding Entries for vector
        sections_entry = ttk.Entry(self.scrollable_frame); sections_entry.grid(row=self.row+2, column=1, sticky = 'w')
        vector = ' '.join([str(elem) for elem in self.vector])
        vector = vector.replace(" ", ", ")
        sections_entry.insert(0, vector)
        self.vector_entries.append(sections_entry)

        # Adding Labels For alpga
        alp_lab = ttk.Label(self.scrollable_frame, text="α:")
        alp_lab.grid(row=self.row+2, column=2, sticky='e')
        self.labels.append(alp_lab)

        # Adding entries for alpha
        alpha_entry = ttk.Entry(self.scrollable_frame); alpha_entry.grid(row=self.row+2, column=3, sticky = 'w')
        alpha_entry.insert(0, self.alpha)
        self.alpha_entries.append(alpha_entry)


        lab = ttk.Label(self.scrollable_frame, text="-"*100, foreground="grey")
        lab.grid(row=self.row+3, column=0, pady = (10,0), columnspan = 5, sticky='w')
        self.labels.append(lab) # Apending to list of labels
        self.row += 3; self.counter += 1 # Increment row number for new section and Increment the number of sections




 
    def add_section(self):

        # Adding Labels For vector
        sec_ent = ttk.Label(self.scrollable_frame, text=f"Section {self.counter}", font = ("bold", 15)); sec_ent.grid(row=self.row+1, column=0, padx=(5,0), pady = (0,10), sticky='w')
        Bn_lab = ttk.Label(self.scrollable_frame, text='Bn')
        Bn_lab.grid(row=self.row+2, column=0,  padx=(5,0), sticky='e')
        self.labels.append(sec_ent); self.labels.append(Bn_lab)

        # Adding Entries for vector
        sections_entry_v = ttk.Entry(self.scrollable_frame, foreground="grey"); sections_entry_v.grid(row=self.row+2, column=1, sticky = 'w')
        random_num_v = round(random.uniform(0,10), 1)
        sections_entry_v.insert(0, random_num_v)
        sections_entry_v.bind("<Button-1>", lambda event: self.clear(sections_entry_v, random_num_v),) # Binding to an event to clear text already in box
        self.vector_entries.append(sections_entry_v)

        # Adding Labels For alpha
        alpha_lab = ttk.Label(self.scrollable_frame, text="α:")
        alpha_lab.grid(row=self.row+2, column=2, sticky='e')
        self.labels.append(alpha_lab)


        # Adding Entries for alpha
        sections_entry_a = ttk.Entry(self.scrollable_frame, foreground="grey"); sections_entry_a.grid(row=self.row+2, column=3, sticky = 'w')
        random_num = round(random.uniform(0,10), 1)
        sections_entry_a.insert(0, random_num)
        sections_entry_a.bind("<Button-1>", lambda event: self.clear(sections_entry_a, random_num),) # Binding to an event to clear text already in box
        self.alpha_entries.append(sections_entry_a)


        lab = ttk.Label(self.scrollable_frame, text="-"*100, foreground="grey")
        lab.grid(row=self.row+3, column=0, pady = (10,0), columnspan = 5, sticky='w')
        self.labels.append(lab) # Apending to list of labels
        self.row += 3; self.counter += 1 # Increment row number for new section and Increment the number of sections

  
    def clear(self, sections_entry, random_num):
        if sections_entry.get() != '':
            if float(sections_entry.get()) == float(random_num):
                sections_entry.delete(0, tk.END) # Deleting text already in box
                sections_entry.config(foreground="white") # Changing colour of the box



    def remove_section(self):
        if self.counter > 1: 
            for i in self.labels[-5:-1]:
                i.destroy()
                self.labels.remove(i)

            self.alpha_entries[-1].destroy()
            self.alpha_entries.pop()
            
            self.vector_entries[-1].destroy()
            self.vector_entries.pop()    
            self.counter -= 1 # Decreasing the counter for every section we remove



    def clear_all(self):

        for i in self.labels[4:]:
            i.destroy()

        for i,j in zip(self.vector_entries[1:], self.alpha_entries[1:]):
            j.destroy()
            i.destroy()
            self.counter -= 1 # Decreasing the counter for every section we remove





    def sum_alpha(self):

        alpha_sum = 0 # Counter to keep track of the current sum of degrees
        user_mistake = False # Flag to keep track of mistakes in the input

        updated_alpha = []
        updated_vector = []


        for i in self.vector_entries:
            vector = i.get()
            updated_vector.append(vector.split(","))


        # Looping through the buttons and getting their alpha value 
        for i in self.alpha_entries:
            alpha = i.get()
            updated_alpha.append(alpha)
            try:
                alpha = float(alpha)
                alpha_sum += float(alpha) # adding to the alpha sum
            except ValueError:
                self.warning_text.set("There is an error in one of your inputs!") # Warning the user
                user_mistake = True # Setting the flag to true since there is a mistake in the input
    
                            
        if alpha_sum > 360:
            self.warning_text.set("The total degrees should not exceed 360 degrees!") # Warning the user if the degrees exceed 360
    
        elif user_mistake == False:
            self.warning_text.set(" ") # Removing the warning if error is fixed
            Pages.alpha_list = updated_alpha
            Pages.vector_list = updated_vector

            print(updated_alpha)
            self.controller.show_frame("PageFive")

