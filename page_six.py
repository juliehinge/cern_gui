
import tkinter as tk      
from tkinter import ttk
from tkinter import *
import numpy as np
import matplotlib.pyplot as plt



class PageSix(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
