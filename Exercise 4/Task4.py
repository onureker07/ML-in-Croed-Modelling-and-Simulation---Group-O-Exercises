import matplotlib.pyplot as plt
import numpy as np
import random

# Set the range of r values to use
r_min = 0
r_max = 4

# Set the number of iterations to use for each value of r
iterations = 100

# Set the initial value of x
x = random.random()

# Create an empty list to store the results
results = []

# Iterate over a range of r values
for r in range(r_min*10000, r_max*10000+1):
  # Reset the value of x for each new value of r
  x = random.random()
  # Iterate for the specified number of iterations
  for i in range(iterations):
    # Update the value of x using the given equation
    x = r/10000 * x * (1 - x)
    # Append the current value of x to the results list
  results.append((r/10000, x))

# Convert the results list to a NumPy array for easier plotting
results = np.array(results)

# Extract the r and x values from the results array
r_values = results[:,0]
x_values = results[:,1]

# Plot the bifurcation diagram
plt.scatter(r_values, x_values, s=1)
plt.xlabel('r')
plt.ylabel('x')
plt.show()

#------------------------------------------------------------#

import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

# Set the parameter values
sigma = 10
beta = 8/3
rhos = [28,0.5]

# Define the function that describes the Lorenz 
for rho in rhos:
  def lorenz(t, y):
    x, y, z = y
    dx = sigma * (y - x)
    dy = x * (rho - z) - y
    dz = x * y - beta * z
    return dx, dy, dz

  # Set the initial values of the system
  x0 = 10
  y0 = 10
  z0 = 10

  # Set the time range to solve for
  t_min = 0
  t_max = 1000

  # Solve for the trajectory of the system
  trajectory = solve_ivp(lorenz, (t_min, t_max), (x0, y0, z0))

  # Extract the solution arrays from the result
  t = trajectory.t
  x = trajectory.y[0]
  y = trajectory.y[1]
  z = trajectory.y[2]

  #Create colormap
  colors = [plt.cm.viridis(z_a/max(z)) for z_a in z]

  # Create a figure and an axis
  fig = plt.figure()
  ax = fig.add_subplot(111, projection='3d')

  # Plot the trajectory
  ax.scatter(x, y, z, s=1, color=colors)
  ax.set_xlabel('x')
  ax.set_ylabel('y')
  ax.set_zlabel('z')

  plt.show()


  # Set the initial values of the system
  x0_changed = 10 + 10**-8
  trajectory = solve_ivp(lorenz, (t_min, t_max), (x0_changed, y0, z0))

  t = trajectory.t
  x_changed = trajectory.y[0]
  y_changed = trajectory.y[1]
  z_changed = trajectory.y[2]
  colors = [plt.cm.viridis(z_a/max(z)) for z_a in z]
  # Create a figure and an axis
  fig = plt.figure()
  ax = fig.add_subplot(111, projection='3d')

  # Plot the trajectory
  ax.scatter(x, y, z, s=1, color=colors)
  ax.set_xlabel('x')
  ax.set_ylabel('y')
  ax.set_zlabel('z')

  plt.show()


  #Eucledian distance for 3d
  def eucledian_distance(x1, y1, z1, x2, y2, z2):
      return np.sqrt((x2-x1)**2 + (y2-y1)**2 + (z2-z1)**2)

  found = False
  differences = []
  for i,time_step in enumerate(t):
      if(not found and eucledian_distance(x[i], y[i], z[i], x_changed[i], y_changed[i], z_changed[i]) > 1):
          found = True
          print("For Rho:",rho,"difference exceed 1 at", time_step)
      differences.append(eucledian_distance(x[i], y[i], z[i], x_changed[i], y_changed[i], z_changed[i]))
  
  plt.plot(t, differences)
  plt.show()

      
          
