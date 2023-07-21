import tkinter as tk
from tkinter import font as tkfont
from tkinter import ttk
from p import Pages
import math

class PageFive(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label1 = tk.Label(self, text="Point Section", font = ("bold", 20))
        label1.grid(row=0, column=0, padx = (10), pady = (10), columnspan=2)
      

        # Labels for instructions
        tk.Label(self, text="please input the coordinate:", font = ("bold", 15)).grid(row=1, column=0, pady=10, sticky='w', )
    

        self.coor_entry = ttk.Entry(self)
        self.coor_entry.grid(row=1, column=1, padx=2, sticky = 'w')


        button1 = ttk.Button(self, text="Back",
                            command=lambda: controller.show_frame("StartPage"))
        button1.grid(row=2, column=0,  pady = (10), sticky='e')


        button2 = ttk.Button(self, text="OK",
                            command=lambda: self.open_next_frame())
        button2.grid(row=2, column=1,  pady = (10), sticky='w')



        self.warning_text = tk.StringVar(self, value=' ')
        self.text = ttk.Label(self, textvariable = self.warning_text, foreground ="red").grid(row=10, column=0,pady = 5, columnspan=3)
        


    def open_next_frame(self):
        print(self.coor_entry.get())

        R = Pages.radius
        B = Pages.vector_list
        A = Pages.alpha_list
        G = [2, -2, 1]
        trims = [[0, math.pi/8], [math.pi/8, 3*math.pi/8], [3*math.pi/8, math.pi/2]]
        P = self.coor_entry.get()

        print(get_B(R, A, B, G, P, trims))


def get_B(R, A, B, G, P, trims):

    # Step 1: check what point it is
    x = P[0]
    y = P[1]
    beta1 = trims[0]
    beta2 = trims[1]
    left_trim_size = 0.138
    right_trim_size = 0.082
    
    # Initialize output
    Bout = 0
    
    # Update output, if needed
    for k in range(len(A)):
        m1 = math.tan(math.pi/2 - A[k][0])
        m2 = math.tan(math.pi/2 - A[k][1])
        
        if y < m1*x - R and y >= m2*x - R:  # if P is in Area k
            if k != len(A) - 1:  # NOT in the last area (exit area)
                d = math.sqrt(x**2 + (y-(-R))**2)
                h = R - d
                Bout = B[k]+ G[k]*h
                break
            elif k == len(A) - 1:  # in the last area (exit area)
                if y >= math.tan(-beta1)*x + (-R-math.tan(-beta1)*(R-left_trim_size)) and \
                        y >= math.tan(beta2)*x + (-R-math.tan(beta2)*(R+right_trim_size)):  # inside magnet
                    d = math.sqrt(x**2 + (y-(-R))**2)
                    h = R - d
                    Bout = B[k] + G[k]*h
                    break
    
    return Bout

