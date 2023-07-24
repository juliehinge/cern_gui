import tkinter as tk
from tkinter import font as tkfont
from ttkthemes import ThemedTk
from start_page import StartPage
from page_one import PageOne
from page_two import PageTwo
from page_three import PageThree
from page_four import PageFour
from page_five import PageFive

# https://stackoverflow.com/questions/39530107/tkinter-have-code-for-pages-in-separate-files
# https://python-forum.io/thread-24731.html


class SampleApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        
        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1); container.grid_columnconfigure(0, weight=1)

        self.frames = {}

 
        for F,geometry in zip((StartPage, PageOne, PageTwo, PageThree, PageFour, PageFive), ('450x500', '450x400', '600x500', '350x150', '600x500', '350x150')):

            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = (frame, geometry)
            frame.grid(row=0, column=0, sticky="nsew")




    
        self.show_frame("StartPage")

    def show_frame(self, page_name):
        frame, geometry = self.frames[page_name]
        self.geometry(geometry)

        frame.event_generate("<<ShowFrame>>")
        frame.tkraise()

 
if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()
