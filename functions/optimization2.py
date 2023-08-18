

import numpy as np
from scipy.optimize import minimize
from functions.map_mag_field import trajectory
from p import Pages
import math
import scipy.optimize


def flatten(li):
    """Flatten the list of lists to a single list."""
    return [item for sublist in li for item in sublist]

def reshape(flat_list):
    """Reshape the flattened list back to the list of lists form."""
    return [flat_list[i:i+2] for i in range(0, len(flat_list), 2)]



def beam_diff(directions, indeces):

    # Caluclate the average particle exit direction of the first beam
    first_key = list(directions.keys())[0]
    first_beam = directions[first_key]
    first_index = list(indeces.values())[0]

    avg_first_beam_particles = []
    for inner_list in first_beam:
        if first_index[0] < len(inner_list):
            avg_first_beam_particles.append(inner_list[first_index[0]])

    average_first_vector = np.mean(avg_first_beam_particles, axis=0)


    # Caluclate the average particle exit direction of the last beam
    last_key = list(directions.keys())[-1]
    last_beam = directions[last_key]
    last_index = list(indeces.values())[-1]

    avg_last_beam_particles = []
    for inner_list in last_beam:
        if last_index[0] < len(inner_list):
            avg_last_beam_particles.append(inner_list[last_index[0]])

    average_last_vector = np.mean(avg_last_beam_particles, axis=0)
   

    # Calculate the dot product
    dot_product = np.dot(average_first_vector, average_last_vector)

    # # Calculate the magnitudes
    mag_first_vector = np.linalg.norm(average_first_vector)
    mag_last_vector = np.linalg.norm(average_last_vector)

    # Calculate the cosine of the angle
    cos_theta = dot_product / (mag_first_vector * mag_last_vector)
    cos_theta = np.clip(cos_theta, -1, 1)

    # Calculate the angle in degrees
    theta = np.arccos(cos_theta) * 180.0 / np.pi


    return abs(theta)



def beam_disparity(directions, index):
    # Flattening the list
    # Calculate the average directional vector
    # Calculate the angles between the average vector and each other vector
    
    angles = []

    dir_at_index = []
    for inner_list in directions:
        if index[0] < len(inner_list):
            dir_at_index.append(inner_list[index[0]])

    average_vector = np.mean(dir_at_index, axis=0)
    for vec in dir_at_index:
        
        # Calculate the dot product
        dot_product = np.dot(average_vector, vec)

        # # Calculate the magnitudes
        mag_average_vector = np.linalg.norm(average_vector)
        mag_v = np.linalg.norm(vec)

        # Calculate the cosine of the angle
        cos_theta = dot_product / (mag_average_vector * mag_v)

        # Calculate the angle in degrees
        cos_theta = np.clip(cos_theta, -1, 1)

        theta = np.arccos(cos_theta) * math.pi/180
        angles.append(abs(theta))
    
    return max(angles)



def exit_size(x_list, y_list, index):

    x_positions = []; y_positions = []

    for x_sublist, y_sublist in zip(x_list, y_list):

        # get the item at 'index' in the sublist
        x_pos = x_sublist[index[0]]
        y_pos = y_sublist[index[0]]

        x_positions.append(x_pos); y_positions.append(y_pos)

    average_x_position = sum(x_positions) / len(x_positions)
    average_y_position = sum(y_positions) / len(y_positions)


    avg_pos = (average_x_position, average_y_position)

    coordinates = list(zip(x_positions, y_positions))

    # calculate the Euclidean distances and find the maximum
    distances = [((x-avg_pos[0])**2 + (y-avg_pos[1])**2)**0.5 for x, y in coordinates]
    max_distance = max(distances)
    max_coordinate = coordinates[distances.index(max_distance)]



    return max_distance




import numpy as np

def objective(params):

   
    # Extract A and li from params
    A = [params[0]]
    flat_li = params[1:]
    li = reshape(flat_li) 
    R = 0.7

    # Get the beam results from the trajectory function
    x, y, _, indices, dd = trajectory(A, li, R)


    # Extract list of filenames (inner keys)
    file_keys = list(x.keys())
    results_beam_sizes = [exit_size(x[file], y[file], indices[file]) for file in file_keys]
    # Computing average beam size
    average_beam_size = sum(results_beam_sizes) / len(results_beam_sizes)

    # Computing beam disparity
    results_beam_disparity = [beam_disparity(dd[file], indices[file]) for file in file_keys]
    average_beam_disparity = sum(results_beam_disparity) / len(results_beam_disparity)



    initial_a = beam_diff(dd, indices)
    initial_b = average_beam_size
    initial_d = average_beam_disparity


    # Ideal parameters
    a = Pages.angle
    b = Pages.beam_size
    d = Pages.beam_divergence


    # Objective function
    f = (initial_a - a)**2 + (initial_b - b)**2 + (initial_d - d)**2
    
    return f




def fmin():

    # Initial guesses
    A_init = Pages.alpha_list
    mag_init = Pages.vector_list

    # Number of rows is based on the length of A_init
    num_rows = len(A_init)
    mag_matrix = np.array(mag_init).reshape(num_rows, -1)
    initial_guess = np.hstack((np.array(A_init).reshape(-1, 1), mag_matrix))

    # Bounds
    A_bounds = (0, 40*math.pi/180)
    li_bounds_1 = (0.4, 0.6)
    li_bounds_2 = (-2.5, 2.5)

    bounds = []
    for i in range(num_rows):
        bounds.append(A_bounds)
        bounds.append(li_bounds_1)
        bounds.append(li_bounds_2)

    print("Initial Guess:", initial_guess.flatten())
    print("Bounds:", bounds)

    # Call minimize
    #solution = minimize(objective, initial_guess.flatten(),bounds=bounds, method='COBYLA')
    solution = scipy.optimize.fmin(objective, initial_guess.flatten())


    print(solution)

    # Extract optimized values
   #if solution.success:
    optimized_values = solution
    # Extract the A values
    optimized_A = [optimized_values[i] for i in range(0, len(optimized_values), 3)]

    # Extract the li values and group them in pairs
    optimized_li = [optimized_values[i:i+2] for i in range(1, len(optimized_values), 3)]

    print("Optimized A:", optimized_A)
    print("Optimized li:", optimized_li)


    x, y, exit, indices, dd = trajectory(optimized_A, optimized_li, Pages.tracking)


    file_keys = list(dd.keys())
    results_beam_sizes = [exit_size(x[file], y[file], indices[file]) for file in file_keys]
    # Computing average beam size
    average_beam_size = sum(results_beam_sizes) / len(results_beam_sizes)
    # Computing beam disparity
    results_beam_disparity = [beam_disparity(dd[file], indices[file]) for file in file_keys]
    average_beam_disparity = sum(results_beam_disparity) / len(results_beam_disparity)
    beam_difference = beam_diff(dd, indices)

    return optimized_A, optimized_li, average_beam_size, average_beam_disparity, beam_difference


