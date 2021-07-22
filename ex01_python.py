# Python's built-in data types are different. [] makes a list. You don't need ;
a = [1,2,3,4]
b = 2*a 

# Looping needs :, and proper indentation
for c in ['q','u','v']:
    print(f"c:{c}")

# For MATLAB like operations, we need Numpy and arrays
# Here the indexing starts with 0, ends with -1
import numpy as np
x = np.arange(0,1000,2)
y = np.sin(2*np.pi*x/250)
z = (x/100)**2

print(f"x[0] = {x[0]}")
print(f"x[-1] = {x[-1]}")
print(f"x.size = {x.size}")


# For plotting, we need matplotlib
from matplotlib import pyplot as plt
fig = plt.figure(1)
plt.subplot(2,1,1)
plt.plot(x, y)
plt.subplot(2,1,2)
plt.plot(x, z)