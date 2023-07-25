import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


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
        m1 = math.tan(math.pi/2 - float(A[k][0]))
        m2 = math.tan(math.pi/2 - float(A[k][1]))
        
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




def default():

    R = 0.7
    a = [0.39, 0.4, 0.5]
    P = [0.2, -0.5]
    trims = [0.1, math.pi/2-0.1 ]
   #li = [[0.6,0.4], [0.5, 2], [-2,1]]
    li = [[1, 0], [0.5, -2], [2,0.3]]


    X_min = -0.2
    X_max = R + 0.5
    Y_min = -R-0.2
    Y_max = 0.2


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
    
    A = []
    curr = 0
    for i in range(len(a)):
        A.append([curr, curr + float(a[i])])
        curr += float(a[i])
    

    X = np.linspace(X_min, X_max, num=100)
    Y = np.linspace(Y_min, Y_max, num=100)
    xx, yy = np.meshgrid(X, Y)


    x_li = []
    y_li = []
    mag_field = []

    for x,y in zip(xx,yy):
        for xx,yy in zip(x,y):
            x_li.append(round(xx,2))
            y_li.append(round(yy,2))
            P = xx, yy
            mag_field.append(get_B(R, A, B, G, P, trims))


    df = pd.DataFrame({

        'x': x_li,
        'y': y_li,
        'values': mag_field
    })

    pivot_table = df.pivot(index='y', columns='x', values='values')
    pivot_table = pivot_table.iloc[::-1] # Reverse the order of rows

    fig, ax = plt.subplots(figsize=(10,7))
    sns.heatmap(pivot_table, cbar_kws={'label': 'B[T]'},cmap="Reds", ax=ax)

    plt.xlabel("X position (m)") 
    plt.ylabel("Y position (m)") 


    a = X_min * min(len(pivot_table.columns), len(pivot_table.index))
    b = Y_min * min(len(pivot_table.columns), len(pivot_table.index))
    r = 0.7

    # Adjust the radius to match the DataFrame indices
    r_adj = r * min(len(pivot_table.columns), len(pivot_table.index))

    stepSize = 0.01

    positions = []
    t = 0
    while t < 2 * math.pi:
        positions.append((r_adj * math.cos(t) + a, r_adj * math.sin(t) + b))
        t += stepSize


    X = []
    Y = []
    for i in positions:
        x, y = i
        X.append(x)
        Y.append(-y)



    ax.plot(X, Y, color='black')


    return fig