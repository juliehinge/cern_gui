import math
import numpy as np
import matplotlib.pyplot as plt
from functions.get_trajectory import get_trajectory
from functions.get_b import get_B
from p import Pages


def get_circle_coordinates(R, a, b, stepSize):
    positions = []
    t = 0
    while t < 2 * math.pi:
        positions.append((R*math.cos(t) + a, R*math.sin(t) + b))
        t += stepSize
    return positions

def create_plot(X, Y):
    fig, ax = plt.subplots(figsize=(10,10)) 
    ax.plot(X, Y, color='black')
    return fig, ax

def split_vectors(li):
    d = dict()
    for i in range(len(li[0])):
        d[i] = []
        for j in range(len(li)):
            try:
                d[i].append(li[j][i])
            except IndexError:
                d[i].append(0)
    B = d[0]
    G = d[1] if 1 in d else [0] * len(li)
    return B, G

def calculate_alpha_intervals(a):
    A = []
    curr = 0
    for i in range(len(a)):
        A.append([curr, curr + float(a[i])])
        curr += float(a[i])
    return A

def map_magnetic_field(X_min, X_max, Y_min, Y_max, R, A, B, G):
    X = np.linspace(X_min, X_max, num=100)
    Y = np.linspace(Y_min, Y_max, num=100)
    xx, yy = np.meshgrid(X, Y)
    mag_field = np.zeros_like(xx)

    for i in range(xx.shape[0]):
        for j in range(xx.shape[1]):
            P = xx[i, j], yy[i, j]
            mag_field[i, j] = get_B(R, A, B, G, P)

    return xx, yy, mag_field




def plot_trajectories(R, A, B, G, directions, positions, Energy):
    for i in range(len(positions)):
        parts = positions[i].split(',')
        pos = [float(part) for part in parts]
        
        parts = directions[i].split(',')
        dir = [float(part) for part in parts]

        x, y, bending_radius = get_trajectory(R, A, B, G, [pos[0],pos[1]], [dir[0],dir[1]], Energy[i], 2)
        plt.plot(x, y)
    
    return bending_radius


def display_magnetic_fild(A, li, R, plot_trajectory=False):
    """ 
    This function creates the default preview that the user can see without having to input X_min, X_max, Y_min, Y_max
    """
    
    X_min, X_max, Y_min, Y_max = -0.2, R + 0.5, -R-0.2, 0.2
    a, b, stepSize = 0, -R, 0.01
    
    positions = get_circle_coordinates(R, a, b, stepSize)
    X = [x for x, y in positions]
    Y = [y for x, y in positions]

    fig, ax = create_plot(X, Y)
    B, G = split_vectors(li)
    A = calculate_alpha_intervals(A)
    xx, yy, mag_field = map_magnetic_field(X_min, X_max, Y_min, Y_max, R, A, B, G)

    color_mesh = ax.pcolormesh(xx, yy, mag_field, cmap='Reds')
    
    ax.set_xlabel('X (m)')
    ax.set_ylabel('Y (m)')
    colorbar = plt.colorbar(color_mesh, ax=ax)
    colorbar.set_label('Magnetic Field (T)')
    ax.set_aspect('equal', adjustable='box')
    ax.set_xlim([X_min, X_max])
    ax.set_ylim([Y_min, Y_max])
    
    bending_radius = None

    if plot_trajectory:
        beams = Pages.file_data

        for file in beams['Energies'].keys():
            energy = beams['Energies'][file]
            positions = beams['Positions'][file]
            directions = beams['Directions'][file]
            energies = flatten_list(beams['Energies'][file])
            
            for j in range(len(positions)):
                x, y, dirs = get_trajectory(R, A, B, G, [positions[j][0], positions[j][1]], [directions[j][0], directions[j][1]], energies[j], Pages.tracking)  # Plotting the beam
                plt.plot(x, y)

    


    return fig, ax, bending_radius




def flatten_list(beams_list):
    return [item for sublist in beams_list for item in sublist]

def calculate_averages(file_data):
    averages = {"Positions": None, "Directions": None, "Energies": None}
    for category, data in file_data.items():
        if category == "Energies":
            averages[category] = sum(val[0] for val in data) / len(data)
        else:
            averages[category] = [sum(val[i] for val in data) / len(data) for i in range(len(data[0]))]
    return averages




def trajectory(A, li, R):
    B, G = split_vectors(li)
    A = calculate_alpha_intervals(A)
    
    
    beams = Pages.file_data
    exit_direction, xx, yy, dd = {}, {}, {}, {}
    indicies = {}

    for file in beams['Energies'].keys():
        energy = beams['Energies'][file]
        positions = beams['Positions'][file]
        directions = beams['Directions'][file]
        energies = flatten_list(energy)

        xx[file], yy[file], dd[file] = [], [], []

        for j in range(len(positions)):
            x, y, dirs = get_trajectory(R, A, B, G, positions[j], directions[j], energies[j], Pages.tracking)
            xx[file].append(x)
            yy[file].append(y)
            dd[file].append(dirs)

        file_data = {'Energies': energy, 'Positions': positions, 'Directions': directions}
        indicies[file] = []

        exit_direction[file] = []
        for j in range(len(positions)):
            averages = calculate_averages(file_data)
            positions = averages['Positions']
            directions = averages['Directions']
            energies = averages['Energies']            
            x, y, dirs = get_trajectory(R, A, B, G, [positions[0], positions[1]], [directions[0], directions[1]], energies, Pages.tracking)  # Plotting the bea
            previous_dir = dirs[-1]
            for i, dir in enumerate(dirs[::-1]):
                if not np.array_equal(dir, previous_dir):
                    indicies[file].append(len(dirs) - i)
                    exit_direction[file].append(dir)
                    break
                previous_dir = dir

    return xx, yy, exit_direction, indicies, dd


