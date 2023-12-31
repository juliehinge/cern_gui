import tkinter as tk
from tkinter import font as tkfont
from pages.start_page import StartPage
from pages.page_one import PageOne
from pages.page_two import PageTwo
from pages.page_three import PageThree
from pages.page_four import PageFour
from pages.page_five import PageFive
from pages.options import Options
from pages.page_six import PageSix
from pages.page_seven import PageSeven
from pages.page_eight import PageEight
from pages.page_ten import PageTen
from pages.page_eleven import PageEleven
from pages.page_fourteen import PageFourteen
from pages.page_fifteen import PageFifteen
from pages.page_sixteen import PageSixteen
from p import Pages
import os
import sys

# Determine the correct path for accessing resources
if getattr(sys, 'frozen', False):
    application_path = sys._MEIPASS
else:
    application_path = os.path.dirname(os.path.abspath(__file__))
start_page_image_path = os.path.join(application_path, 'gui_figure1.png')

class SampleApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        
        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F, geometry in zip((StartPage, PageOne, PageTwo, PageThree, PageFour, PageFive, Options, PageSix, PageSeven, PageEight, PageTen, PageEleven, PageFourteen, PageFifteen, PageSixteen), 
                               ('450x500', '400x350', '600x500', '350x150', '600x500', '600x500', '300x300', '600x600', '600x600', '500x450', '950x700', '700x500',  '600x600', '600x600', '700x700')):
            
            page_name = F.__name__
            if F == StartPage:
                frame = F(parent=container, controller=self, image_path=start_page_image_path)
            else:
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