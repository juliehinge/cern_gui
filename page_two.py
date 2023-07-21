import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkscrolledframe import ScrolledFrame
import random
from p import Pages


class PageTwo(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)

        # Create the scrollable frame
        self.sf = ScrolledFrame(self.container, width=640, height=400, scrollbars="vertical")
        self.sf.pack(fill="both", expand=True)
    
        self.sf.bind_arrow_keys(self.container); self.sf.bind_scroll_wheel(self.container)

        self.scrollable_frame = self.sf.display_widget(tk.Frame)



        label = tk.Label(self.scrollable_frame, text="Input information about the vectors please", font=("bold", 20))
        label.grid(row=0, column=0, padx=(10, 30), pady=(10, 20), sticky='w', columnspan=4)

        ttk.Label(self.scrollable_frame, text="-" * 100, foreground="grey").grid(row=1, column=0, pady=(10, 0),
                                                                                      columnspan=4, sticky='w')
      
        # Counters for row number and number of sections
        self.row = 1; self.counter = 0  
        self.alpha_entries = []; self.vector_entries = []; self.labels = [] # Lists to keep track of all the widgets

        # Adding the first section
        self.add_section()

        # Create the frame at the bottom
        self.bottom_frame = tk.Frame(self.container)
        self.bottom_frame.pack(side="bottom")

        self.btn_add = ttk.Button(self.bottom_frame, text="Add Section", command=self.add_section)
        self.btn_add.grid(row=0, column=0, padx=5, pady=5)

        self.btn_remove = ttk.Button(self.bottom_frame, text="Remove Section", command=self.remove_section)
        self.btn_remove.grid(row=0, column=1, padx=5, pady=5)

        self.btn_clear = ttk.Button(self.bottom_frame, text="Clear All", command=self.clear_all)
        self.btn_clear.grid(row=0, column=2, padx=5, pady=5)

        self.btn_ok = ttk.Button(self.bottom_frame, text="OK", width=5, command=self.sum_alpha)
        self.btn_ok.grid(row=0, column=3, padx=5, pady=5)

        self.btn_back = ttk.Button(self.bottom_frame, text="Back",
                            command=lambda: controller.show_frame("PageOne"))
        self.btn_back.grid(row=0, column=4, padx=5, pady=5)


        self.warning_text = StringVar(self.bottom_frame, value=' ')
        self.text = ttk.Label(self.bottom_frame, textvariable=self.warning_text, foreground="red")
        self.text.grid(row=1, column=0, columnspan=5, padx=5, pady=5)




    def add_section(self):
        i = self.row
        self.vector_section(i)
        self.alpha_section(i)
        lab = ttk.Label(self.scrollable_frame, text="-" * 100, foreground="grey")
        lab.grid(row=i + 3, column=0, pady=(10, 0), columnspan=5, sticky='w')
        self.labels.append(lab)
        self.row += 3
        self.counter += 1


    def vector_section(self, i):
        lab1 = ttk.Label(self.scrollable_frame, text=f"Section {self.counter + 1}", font=("bold", 15))
        lab1.grid(row=self.row + 1, column=0, pady=(0, 10), sticky='w', columnspan=4)
        lab2 = ttk.Label(self.scrollable_frame, text='Bn:')
        lab2.grid(row=self.row + 2, column=0, sticky='e')
        self.labels.append(lab1)
        self.labels.append(lab2)

        sections_entry = ttk.Entry(self.scrollable_frame, foreground="grey")
        sections_entry.grid(row=self.row + 2, column=1, sticky='w')
        random_num = random.randint(0, 9)
        sections_entry.insert(0, random_num)
        sections_entry.bind("<Button-1>", lambda event: self.clear(sections_entry))
        self.vector_entries.append(sections_entry)
        lab3 = tk.Label(self.scrollable_frame, text="α:", font=(10))
        lab3.grid(row=self.row + 2, column=2, sticky='e', padx=(10, 0))
        self.labels.append(lab3)



    def alpha_section(self, i):
        sections_entry = ttk.Entry(self.scrollable_frame, foreground="grey")
        sections_entry.grid(row=self.row + 2, column=3, sticky='w')
        random_num = random.randint(0, 360)
        sections_entry.insert(0, random_num)
        sections_entry.bind("<Button-1>", lambda event: self.clear(sections_entry))
        self.alpha_entries.append(sections_entry)



    def clear(self, sections_entry):
        sections_entry.delete(0, tk.END)
        sections_entry.config(foreground="white")


    def remove_section(self):
        if self.counter > 1:
            for i in self.labels[-5:-1]:
                i.destroy()
                self.labels.remove(i)

            self.alpha_entries[-1].destroy()
            self.alpha_entries.pop()

            self.vector_entries[-1].destroy()
            self.vector_entries.pop()
            self.counter -= 1


    def clear_all(self):
        for i in self.labels[3:]:
            i.destroy()

        for i, j in zip(self.vector_entries[1:], self.alpha_entries[1:]):
            j.destroy()
            i.destroy()
            self.counter -= 1

        ttk.Label(self.scrollable_frame, text="-" * 100, foreground="grey").grid(row=self.row, column=0, pady=(10, 0),
                                                                                  columnspan=5, sticky='w')

    def sum_alpha(self):
        alpha_sum = 0
        user_mistake = False
        self.warning_text.set("")

        for i in self.alpha_entries:
            alpha = i.get()
            if not alpha.isnumeric():
                self.warning_text.set("There is an error in one of your inputs!")
                user_mistake = True
            else:
                alpha_sum += int(alpha)

        if alpha_sum > 360:
            self.warning_text.set("The total degrees should not exceed 360 degrees!")
        elif not user_mistake:
            self.warning_text.set("")
            Pages.alpha_list = self.alpha_entries
            Pages.vector_list = self.vector_entries
            self.controller.show_frame("PageFive")

        


if __name__ == "__main__":
    app = PageTwo(None, None)
    app.mainloop()