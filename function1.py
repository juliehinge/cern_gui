import math


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

import math

R = 0.7
A = [[0, math.pi/8], [math.pi/8, 3*math.pi/8], [3*math.pi/8, math.pi/2]]
B = [0.6, 0.4, 0.5]
G = [2, -2, 1]
P = [0.2, -0.5]
trims = [0.1, math.pi/2-0.1 ]



li = [[0.6, 2], [0.4,-2], [0.5,1]]

for pol in B[0]:
    print(pol)
















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
                    
                    print(beta1)

                    d = math.sqrt(x**2 + (y-(-R))**2)
                    h = R - d
                    Bout = B[k] + G[k]*h
                    break
    
    return Bout


#print(get_B(R, A, B, G, P, trims))