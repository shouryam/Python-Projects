#
#  Simple python random walk in 1D
#  Plots histogram of ending positions
#
import random
import numpy as np
import matplotlib.pyplot as plt

def random_walk(steps):
    """  Performs 1D random walk with number steps = steps """
    walk = np.zeros(steps+1)
    for i in range(steps):
        if random.uniform(0, 1) < .5:
            step =  1
        else:
            step = -1
        walk[i+1] = walk[i] + random.choice([-1,1])
    return walk

num_walks = int(input("
num_steps = 1000 
#
#  Perform random walks and saves ending step
# 
last_pos = np.zeros(num_walks)
for i in range(num_walks):      
    walk = random_walk(num_steps)
    last_pos[i] = walk[-1] 
#************************************
#   YOUR CODE goes HERE:
#    Compute the average of the last
#    positions (from last position array
#    above) and store in variable called:
#      'ave_dist2' . This variable is 
#   used in plot below   
#
ave_dist2 = np.average(last_pos**2)
#***********************************88

print ' For %d steps, average distance squared from center = %5.1f' %( num_steps, ave_dist2)
#  Set plot title , legend, and grid 
plt.title('Histogram of 1D walk , #steps = %i, <x**2> = %6.1f' % (num_steps, ave_dist2))
plt.hist(last_pos, bins=50, color='red') 
plt.xlabel(' Number of steps')
plt.ylabel(' Frequency')
plt.savefig('hist' + str(num_steps) + '.png')
plt.grid(True)
plt.show() 
