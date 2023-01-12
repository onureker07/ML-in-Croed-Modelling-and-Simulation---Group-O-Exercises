import numpy as np
import matplotlib.pyplot as plt

# Load the data from the file
data = np.loadtxt("takens_1.txt")

# Extract the first column (coordinate 1)
coord1 = data[:,0]

# Plot the first coordinate against the line number
plt.plot(coord1)
plt.xlabel("Line number (time)")
plt.ylabel("First coordinate")
plt.show()

# Choose a delay of n rows
n = 10

# Create a new array with the delayed coordinate
coord1_delayed = np.array([coord1[i] for i in range(n, len(coord1))])

# Plot the original coordinate against the delayed coordinate
plt.plot(coord1[:-n], coord1_delayed)
plt.xlabel("First coordinate")
plt.ylabel("First coordinate (delayed by n)")
plt.show()
