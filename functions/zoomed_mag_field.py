

import math
import numpy as np
import matplotlib.pyplot as plt
from functions.get_b import get_B


def get_circle_coordinates(R):
    a = 0
    b = -R
    stepSize = 0.01
    positions = []
    t = 0
    while t < 2 * math.pi:
        positions.append((R*math.cos(t) + a, R*math.sin(t) + b))
        t += stepSize
    X = [x for x, y in positions]
    Y = [y for x, y in positions]
    return X, Y

def split_vectors(li):
    d = dict()
    for i in range(len(li[0])):
        d[i] = [li[j][i] if j < len(li) and i < len(li[j]) else 0 for j in range(len(li))]
    B = d.get(0, [])
    G = d.get(1, [0] * len(li))
    return B, G

def calculate_alpha_intervals(a):
    A = []
    curr = 0
    for alpha in a:
        A.append([curr, curr + float(alpha)])
        curr += float(alpha)
    return A

def calculate_magnetic_field(X_min, X_max, Y_min, Y_max, R, A, B, G):
    X = np.linspace(X_min, X_max, num=100)
    Y = np.linspace(Y_min, Y_max, num=100)
    xx, yy = np.meshgrid(X, Y)
    mag_field = np.zeros_like(xx)
    for i in range(xx.shape[0]):
        for j in range(xx.shape[1]):
            P = xx[i, j], yy[i, j]
            mag_field[i, j] = get_B(R, A, B, G, P)
    return xx, yy, mag_field

def zoomed_preview(X_min, X_max, Y_min, Y_max, A, li, R):
    """This function creates the custom view that the user can see after inputting X_min, X_max, Y_min, Y_max"""

    X, Y = get_circle_coordinates(R)
    fig, ax = plt.subplots(figsize=(10,10))
    ax.plot(X, Y, color='black')

    B, G = split_vectors(li)
    A = calculate_alpha_intervals(A)
    xx, yy, mag_field = calculate_magnetic_field(X_min, X_max, Y_min, Y_max, R, A, B, G)
    
    color_mesh = ax.pcolormesh(xx, yy, mag_field, cmap='Reds')
    
    ax.set_xlabel('X (m)')
    ax.set_ylabel('Y (m)')
    colorbar = plt.colorbar(color_mesh, ax=ax)
    colorbar.set_label('Magnetic Field (T)')
    ax.set_aspect('equal', adjustable='box')
    ax.set_xlim([X_min, X_max])
    ax.set_ylim([Y_min, Y_max])
    
    return fig
