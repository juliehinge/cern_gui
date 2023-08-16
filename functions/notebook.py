import numpy as np
import math
from p import Pages
import matplotlib.pyplot as plt
from scipy.optimize import minimize




def get_B(R, A, B, G, P):
    # Step 1: check what point it is
    x = P[0]
    y = P[1]

    # Initialize output
    Bout = 0
    # Update output, if needed
    for k in range(len(A)):
        
        m1 = math.tan(math.pi/2 - float(A[k][0]))
        m2 = math.tan(math.pi/2 - float(A[k][1]))
        
        if y < m1*x - R and y >= m2*x - R:  # if P is in Area k

            d = math.sqrt(x**2 + (y-(-R))**2)
            h = R - d
            Bout = float(B[k]) + float(G[k])*h
            break
 
    return Bout



def rot_matrix(alpha):
    R = np.array([[np.cos(alpha), -np.sin(alpha)],
        [np.sin(alpha), np.cos(alpha)]]) # Defining the rotation matrix in a clockwise direction
    return R


def next_point(r, P, D):
    
    s = 0.01 # Step size

   
    pc = np.matmul(rot_matrix(-math.pi/2), D) # Multiplying the two matrices together to get the vector going from the point to the center
    pc = r *pc 

    Cx = P[0]+pc[0]
    Cy = P[1]+pc[1]
    c = np.array([Cx, Cy])
   
    CP = np.subtract(P, c) # Subtracting the center from the point to find CP
    r += 1e-10
    theta = s/r
  
    CP2 = np.matmul(rot_matrix(-theta), CP)
    P2 = np.add(c,CP2) # Adding the distance from the center of the circle with the coordinates of the center to find the coordinates of the new point

    PC2 = -CP2
    D2 = np.matmul(rot_matrix(math.pi/2), PC2)

    # Compute the magnitude of the vector
    magnitude = np.linalg.norm(D2) 
    # Normalize the vector
    D2 = D2/magnitude  


    return P2, D2   




def get_points(R, A, B, G, P, D, Energy, size):

    # Compute the magnitude of the vector for normalization
    magnitude = np.linalg.norm(D) 
    # Normalize the vector
    eps = 1e-10
    D = D/(magnitude+eps) # Normalizing the vector and adding a tiny constant to avoid division by zero error

    B_e = 3.3356*(Energy/1000) # Beam Rigidity
    s = 0.01 # Step size

    points = []
    points.append([float(P[0]), float(P[1])])

    directions = []

    trajectory_len = float(size)
    num_steps = trajectory_len/s

    for i in range(int(num_steps)):

        Bout = get_B(R, A, B, G, P)
        if Bout != 0:
            bending_rad = abs(B_e/Bout) # Radius
            P, D = next_point(bending_rad,P,D) # Calculating the next point
        else: # If the magnetic field is zero at this point the particle just continues in a straight line
            P2 = s*D
            P = np.add(P, P2)

        points.append(P)
        directions.append(D)
     
    # Splitting the data into x and y coordinates for plotting
    x = [point[0] for point in points]
    y = [point[1] for point in points]


    return x,y,directions







def default2(A, li, R):
    """ This function creates the default preview that the user can see without having to input X_min, X_max, Y_min, Y_max"""


    X_min = -0.4
    X_max = R + 0.7
    Y_min = -R-0.4
    Y_max = 0.2
    a = 0 # X coordinate of center of circle
    b = -R # Y coordinate of center of circle
    stepSize = 0.001 # Stepsize of line of circle

    # This is to calculate the coordinates of the circles circumference
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

    # Initiating the plot
    fig, ax = plt.subplots(figsize=(10,10)) 

    # Adding the line to the plot
    ax.plot(X, Y, color='black')

    # This is to split the Vector into B and G
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
    except KeyError: # If the user only input vector of size one, we just make G a vector of 0's
        G = []
        for i in range(len(li)):
            G.append(0)

    a = A # This is just to not confuse the old alpha with the "new"
    A = []
    curr = 0
    # This part calculates the beginning point and end point of alpha
    for i in range(len(a)):
        A.append([curr, curr + float(a[i])])
        curr += float(a[i])


    # This makes the coordinates of the points and initiates the magnetic field vector
    X = np.linspace(X_min, X_max, num=100)
    Y = np.linspace(Y_min, Y_max, num=100)
    xx, yy = np.meshgrid(X, Y)
    mag_field = np.zeros_like(xx)

    for i in range(xx.shape[0]):
        for j in range(xx.shape[1]):
            P = xx[i, j], yy[i, j] # Here we define the coordinates of the point
            mag_field[i, j] = get_B(R, A, B, G, P) # Here we calculate the magnetic field at position P

    color_mesh = ax.pcolormesh(xx, yy, mag_field, cmap='Reds') # This line makes the actual plot

    # This is just for customizing the look of the plot
    ax.set_xlabel('X (m)')
    ax.set_ylabel('Y (m)')
    colorbar = plt.colorbar(color_mesh, ax=ax)
    colorbar.set_label('Magnetic Field (T)')
    ax.set_aspect('equal', adjustable='box')
    ax.set_xlim([X_min, X_max])
    ax.set_ylim([Y_min, Y_max])
    



    beams = Pages.file_data
        

    def flatten_list(beams_list):
        return [item for sublist in beams_list for item in sublist]

    exit_direction = {}
    xx = {}
    yy ={} 
    dd = {} 

    all_x = {}
    all_y = {}
    all_d_x = {}

    indicies = {}





    def calculate_averages(file_data):
        averages = {"Positions": None, "Directions": None, "Energies": None}

        for category, data in file_data.items():
            if category == "Energies":
                averages[category] = sum(val[0] for val in data) / len(data)
            else:
                averages[category] = [sum(val[i] for val in data) / len(data) for i in range(len(data[0]))]

        return averages



    for file in beams['Energies'].keys():

        energy = beams['Energies'][file]
        positions = beams['Positions'][file]
        directions = beams['Directions'][file]
        energies = flatten_list(beams['Energies'][file])

        xx[file] = []
        yy[file] = []
        dd[file] = []

        for j in range(len(positions)):
            x, y, dirs = get_points(R, A, B, G, [positions[j][0], positions[j][1]], [directions[j][0], directions[j][1]], energies[j], 1.7)  # Plotting the beam
            plt.plot(x,y)
            xx[file].append(x); yy[file].append(y); dd[file].append(dirs)

        file_data = {'Energies': energy, 'Positions': positions, 'Directions': directions}


     
        exit_direction[file] = []
        all_x[file] = []
        all_y[file] = []
        all_d_x[file] = []

        indicies[file] = []

        for j in range(len(positions)):

            averages = calculate_averages(file_data)
            positions = averages['Positions']
            directions = averages['Directions']
            energies = averages['Energies']

            x, y, dirs = get_points(R, A, B, G, [positions[0], positions[1]], [directions[0], directions[1]], energies, 1.7)  # Plotting the beam

            first_and_second_elements = [list(arr[:2]) for arr in dirs]


            previous_dir = dirs[-1]
            for i, dir in enumerate(dirs[::-1]):
                if not np.array_equal(dir, previous_dir):
                    ax.scatter(x[len(dirs) - i], y[len(dirs) - i])
                    indicies[file].append(len(dirs) - i)
                    exit_direction[file].append(dir)
                    all_x[file].append(x)
                    all_y[file].append(y)
                    all_d_x[file].append(first_and_second_elements)
                    break
                previous_dir = dir

            break


    
    return fig, ax, xx, yy, exit_direction, indicies, dd







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

        # Calculate the angle in radians
        cos_theta = np.clip(cos_theta, -1, 1)

        theta = np.arccos(cos_theta) * (180.0 / np.pi)
        angles.append(abs(theta))
    
    return max(angles)




def beam_diff(beam_exit_directions, indeces):

    # Caluclate the average particle exit direction of the first beam
    first_key = list(beam_exit_directions.keys())[0]
    first_beam = beam_exit_directions[first_key]
    first_index = list(indeces.values())[0]

    avg_first_beam_particles = []
    for inner_list in first_beam:
   
        if first_index[0] < len(inner_list):
            avg_first_beam_particles.append(inner_list[first_index[0]])

    average_first_vector = np.mean(avg_first_beam_particles, axis=0)



    # Caluclate the average particle exit direction of the last beam
    last_key = list(beam_exit_directions.keys())[-1]
    last_beam = beam_exit_directions[last_key]
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

    # Calculate the angle in radians
    theta = np.arccos(cos_theta) * (180.0 / np.pi)


    return abs(theta)







def trajectory(A, li, R):
    """ This function creates the default preview that the user can see without having to input X_min, X_max, Y_min, Y_max"""



    # Default values for x_min, x_max, y_min, y_max
    X_min = -0.4
    X_max = R + 0.7
    Y_min = -R-0.4
    Y_max = 0.2
    a = 0 # X coordinate of center of circle
    b = -R # Y coordinate of center of circle
    stepSize = 0.001 # Stepsize of line of circle




    # This is to split the Vector into B and G
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
    except KeyError: # If the user only input vector of size one, we just make G a vector of 0's
        G = []
        for i in range(len(li)):
            G.append(0)

    a = A # This is just to not confuse the old alpha with the "new"
    A = []
    curr = 0
    # This part calculates the beginning point and end point of alpha
    for i in range(len(a)):
        A.append([curr, curr + float(a[i])])
        curr += float(a[i])



    # This makes the coordinates of the points and initiates the magnetic field vector
    X = np.linspace(X_min, X_max, num=100)
    Y = np.linspace(Y_min, Y_max, num=100)
    xx, yy = np.meshgrid(X, Y)
    mag_field = np.zeros_like(xx)

    for i in range(xx.shape[0]):
        for j in range(xx.shape[1]):
            P = xx[i, j], yy[i, j] # Here we define the coordinates of the point
            mag_field[i, j] = get_B(R, A, B, G, P) # Here we calculate the magnetic field at position P







    beams = Pages.file_data

    def flatten_list(beams_list):
        return [item for sublist in beams_list for item in sublist]

    exit_direction = {}
    xx = {}
    yy ={} 
    dd = {} 
    indicies = {}



    def calculate_averages(file_data):
        averages = {"Positions": None, "Directions": None, "Energies": None}

        for category, data in file_data.items():
            if category == "Energies":
                averages[category] = sum(val[0] for val in data) / len(data)
            else:
                averages[category] = [sum(val[i] for val in data) / len(data) for i in range(len(data[0]))]

        return averages



    for file in beams['Energies'].keys():

        energy = beams['Energies'][file]
        positions = beams['Positions'][file]
        directions = beams['Directions'][file]
        energies = flatten_list(beams['Energies'][file])

        xx[file] = []
        yy[file] = []
        dd[file] = []

        for j in range(len(positions)):
            x, y, dirs = get_points(R, A, B, G, [positions[j][0], positions[j][1]], [directions[j][0], directions[j][1]], energies[j], 1.7)  # Plotting the beam
           # plt.plot(x,y)
            xx[file].append(x); yy[file].append(y); dd[file].append(dirs)

        file_data = {'Energies': energy, 'Positions': positions, 'Directions': directions}

     
        exit_direction[file] = []
   
        indicies[file] = []

        for j in range(len(positions)):

            averages = calculate_averages(file_data)
            positions = averages['Positions']
            directions = averages['Directions']
            energies = averages['Energies']

            x, y, dirs = get_points(R, A, B, G, [positions[0], positions[1]], [directions[0], directions[1]], energies, 1.7)  # Plotting the bea


            previous_dir = dirs[-1]
            direction_changed = False
            
            # Iterate through the directions in reverse order
            for i, dir in enumerate(dirs[::-1]):
                # If the current direction does not match the previous direction
                if not np.array_equal(dir, previous_dir):
                    # Append the index where direction changes to the indices dictionary for the current file
                    indicies[file].append(len(dirs) - i)
                    # Append the changed direction to the exit_direction dictionary for the current file
                    exit_direction[file].append(dir)
                    # Break out of the loop after finding the first change in direction
                    direction_changed = True
                    break
                # Update the previous_dir for the next iteration
                previous_dir = dir
            if not direction_changed:
                indicies[file].append(len(dirs) - 1)
                exit_direction[file].append(dirs[-1])

    return xx, yy, exit_direction, indicies, dd







def flatten(li):
    """Flatten the list of lists to a single list."""
    return [item for sublist in li for item in sublist]

def reshape(flat_list):
    """Reshape the flattened list back to the list of lists form."""
    return [flat_list[i:i+2] for i in range(0, len(flat_list), 2)]





def objective(params):

   
    # Extract A and li from params
    A = [params[0]]
    flat_li = params[1:]
    li = reshape(flat_li) 
    R = 0.7

    # Get the beam results from the default2 function
    x, y, _, indices, dd = trajectory(A, li, R)


    file_keys = list(dd.keys())
    results_beam_sizes = [exit_size(x[file], y[file], indices[file]) for file in file_keys]
    # Computing average beam size
    average_beam_size = sum(results_beam_sizes) / len(results_beam_sizes)
    # Computing beam disparity
    results_beam_disparity = [beam_disparity(dd[file], indices[file]) for file in file_keys]
    average_beam_disparity = sum(results_beam_disparity) / len(results_beam_disparity)



    average_beam_disparity = sum(results_beam_disparity) / len(results_beam_disparity)


    initial_a = beam_diff(dd, indices)
    initial_b = average_beam_size
    initial_d = average_beam_disparity

    a = Pages.angle
    b = Pages.beam_size
    d = Pages.beam_divergence



    # Objective function
    f = (initial_a - a)**2 + (initial_b - b)**2 + 50*(initial_d - d)**2
    
    return f






def fmin():

    # Initial guesses
    # Initial guesses
    A_init = [0.6, 0.95]
    mag_init = [[0.57, -0.7], [0.57, 2.4]]

    # Number of rows is based on the length of A_init
    num_rows = len(A_init)
    mag_matrix = np.array(mag_init).reshape(num_rows, -1)
    initial_guess = np.hstack((np.array(A_init).reshape(-1, 1), mag_matrix))

    # Bounds
    A_bounds = (0, 40*math.pi/180)
    li_bounds_1 = (0, 2)
    li_bounds_2 = (-2, 2)

    A_bounds_list = [A_bounds] * len(A_init)
    li_bounds_list = [li_bounds_1, li_bounds_2] * num_rows
    bounds = A_bounds_list + li_bounds_list


    print("Initial Guess:", initial_guess)
    print("Bounds:", bounds)

    # Call minimize
    #solution = minimize(objective, initial_guess.flatten(), bounds=bounds, method='COBYLA')

    options = {'rhobeg': 1.5}  # Adjust 0.5 to your desired initial step size
    solution = minimize(objective, initial_guess.flatten(), bounds=bounds, method='COBYLA', options=options)



    # Extract optimized values
    if solution.success:
        optimized_values = solution.x
        optimized_A = optimized_values[:2]
        optimized_li = optimized_values[2:].reshape(num_rows, -1)
        print("Optimized A:", optimized_A)
        print("Optimized li:", optimized_li)
    

        #x, y, exit, indices, dd = trajectory(optimized_A, optimized_li, Pages.tracking)
        fig, ax, x, y, exit, indices, dd = default2(optimized_A, optimized_li, Pages.tracking)

        file_keys = list(dd.keys())
        results_beam_sizes = [exit_size(x[file], y[file], indices[file]) for file in file_keys]
        # Computing average beam size
        average_beam_size = sum(results_beam_sizes) / len(results_beam_sizes)
        # Computing beam disparity
        results_beam_disparity = [beam_disparity(dd[file], indices[file]) for file in file_keys]
        average_beam_disparity = sum(results_beam_disparity) / len(results_beam_disparity)
        beam_difference = beam_diff(dd, indices)

        return optimized_A, optimized_li, average_beam_size, average_beam_disparity, beam_difference

    else:
        print("Optimization did not converge:", solution.message)
