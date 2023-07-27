import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from p import Pages

"""""
   INPUT variables:
      % R: ref. bending radius, in m.
      %                           Ex: R = 0.7
      % A: section angles [start, end], in rad.
      %                           Ex: A = [ 0 pi/8; pi/8 3*pi/8; 3*pi/8 pi/2 ]
      % B: dipole field component per section, in T.
      %                           Ex: B = [ 0.6, 0.4, 0.5 ]
      % G: quadrupole field component per section, in T/m.
      %                           Ex: G = [ 2, -2, 1 ]
      % P = [x,y]: point to evaluate the B field, in m.
      %                           Ex: P = [ 0.2, -0.5]
      % trims: angles of the exit trims, in rad.
      %                           Ex: trims = [ 0.1 pi/2-0.1 ]
  % OUTPUT variables:
      % Bout: magnitude of the mag. field in the z direction at point P, in T.

  """



def get_B(R, A, B, G, P):
    # Step 1: check what point it is
    x = P[0]
    y = P[1]
   # beta1 = trims[0]
   # beta2 = trims[1]
   # left_trim_size = 0.138
   # right_trim_size = 0.082
    
    # Initialize output
    Bout = 0
    
    # Update output, if needed
    for k in range(len(A)):
        m1 = math.tan(math.pi/2 - float(A[k][0]))
        m2 = math.tan(math.pi/2 - float(A[k][1]))
        
        if y < m1*x - R and y >= m2*x - R:  # if P is in Area k
            d = math.sqrt(x**2 + (y-(-R))**2)
            h = R - d

            Bout = float(B[k])+ float(G[k])*h
            break


    return Bout








import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math

def custom(X_min, X_max, Y_min, Y_max, A, li, R):
    a = 0 
    b = -R
    r = 0.5
    stepSize = 0.01

    positions = []
    t = 0
    while t < 2 * math.pi:
        positions.append((R*math.cos(t) + a, R*math.sin(t) + b))
        t += stepSize

    X = []
    Y = []
    for i in positions:
        x, y = i
        X.append(x)
        Y.append(y)

    fig, ax = plt.subplots(figsize=(10,10)) 
    ax.plot(X, Y, color='black')

    # helper function part starts here
    d = dict()
    for i in range(len(li[0])):
        d[i] = []
        for j in range(len(li)):
            try:
                d[i].append(li[j][i])
            except IndexError:
                d[i].append(0)
    B = d[0]
    try:
        G = d[1]
    except KeyError:
        G = []
        for i in range(len(li)):
            G.append(0)
    a = A
    A = []
    curr = 0
    for i in range(len(a)):
        A.append([curr, curr + float(a[i])])
        curr += float(a[i])

    X = np.linspace(X_min, X_max, num=100)
    Y = np.linspace(Y_min, Y_max, num=100)
    xx, yy = np.meshgrid(X, Y)

    mag_field = np.zeros_like(xx)

    for i in range(xx.shape[0]):
        for j in range(xx.shape[1]):
            P = xx[i, j], yy[i, j]
            mag_field[i, j] = get_B(R, A, B, G, P)

    color_mesh = ax.pcolormesh(xx, yy, mag_field, cmap='Reds')

    ax.set_xlabel('X (m)')
    ax.set_ylabel('Y (m)')

    colorbar = plt.colorbar(color_mesh, ax=ax)
    colorbar.set_label('Magnetic Field (T)')
    # helper function part ends here

    ax.set_aspect('equal', adjustable='box')
    ax.set_xlim([X_min, X_max])
    ax.set_ylim([Y_min, Y_max])

    return fig  # return only figure object
def default(A, li, R):
    X_min = -0.2
    X_max = R + 0.5
    Y_min = -R-0.2
    Y_max = 0.2

    a = 0 
    b = -R
    r = 0.5
    stepSize = 0.01

    positions = []
    t = 0
    while t < 2 * math.pi:
        positions.append((R*math.cos(t) + a, R*math.sin(t) + b))
        t += stepSize

    X = []
    Y = []
    for i in positions:
        x, y = i
        X.append(x)
        Y.append(y)

    fig, ax = plt.subplots(figsize=(10,10)) 
    ax.plot(X, Y, color='black')

    # helper function part starts here
    d = dict()
    for i in range(len(li[0])):
        d[i] = []
        for j in range(len(li)):
            try:
                d[i].append(li[j][i])
            except IndexError:
                d[i].append(0)
    B = d[0]
    try:
        G = d[1]
    except KeyError:
        G = []
        for i in range(len(li)):
            G.append(0)
    a = A
    A = []
    curr = 0
    for i in range(len(a)):
        A.append([curr, curr + float(a[i])])
        curr += float(a[i])

    X = np.linspace(X_min, X_max, num=500)
    Y = np.linspace(Y_min, Y_max, num=500)
    xx, yy = np.meshgrid(X, Y)

    mag_field = np.zeros_like(xx)

    for i in range(xx.shape[0]):
        for j in range(xx.shape[1]):
            P = xx[i, j], yy[i, j]
            mag_field[i, j] = get_B(R, A, B, G, P)

    color_mesh = ax.pcolormesh(xx, yy, mag_field, cmap='Reds')

    ax.set_xlabel('X (m)')
    ax.set_ylabel('Y (m)')

    colorbar = plt.colorbar(color_mesh, ax=ax)
    colorbar.set_label('Magnetic Field (T)')
    # helper function part ends here

    ax.set_aspect('equal', adjustable='box')
    ax.set_xlim([X_min, X_max])
    ax.set_ylim([Y_min, Y_max])

    return fig  # return only figure object
