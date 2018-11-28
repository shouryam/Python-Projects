#
#  Executes target seeking random walk inside a
#  confining boundary. Conducts and 
#   plots up to 5 random walks
#
#  Following parameters can be specified:
#    1- Shape, size, and location of boundary
#    2- Shape, size, and location of target
#    3- Random step type (continuous angle or on a grid) 
#    4 -Starting location for random walk 
#    5 -Choice of 1) grid or 2) continuous angle random steps
#
import sys, random
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt
import shapes3d_class as shapes
import randwalk3d_class as rw3d

random.seed(None)        # Seed generator, None => system clock
#
#   Enter number of walks to simulate
#
num_sim = int(raw_input('Enter number of simulations to run:  '))
#   Sets maximum number of steps in each random walk    
max_steps = 50000
#
#  Set boundary shape and location
#  Choices are defined in shapes3d_class:  
#         Sphere( (x,y,z), radius)   
#         Rectangle3d( (x,y,z), width,depth, height)
#         Ellipsoid( (x,y,z) , a , b, c) 
#  where (x,y, z) is center of shape  and a,b,c are axes of ellipsoid
#
boundary      = shapes.Ellipsoid((0.0, 0.0, 0.0), 20, 40, 20) 
#    boundary  = shapes.Rectangle3d((0.0, 0.0,0.0), 20, 20, 40)
#    boundary  = shapes.Sphere((0.0, 0.0, 0.0), 30)
#
#  Set target shape and initial location (see shape choices above)
#
target_loc = (5.0, 5.0, 5.0)
#target = shapes.Rectangle3d(target_loc, 4 , 4, 4) 
target = shapes.Sphere(target_loc, 3)
# 
#  Select random function (rand_direct or rand_grid)
#
rand_function = rw3d.rand_direct
#    rand_function = rw3d.rand_grid
#
#  Assign starting location for walks and move_target_flag
#   and compute initial distance from start to target location
# start_loc   = (0.0,0.0,0.0)
start_loc   = (0.0,0.0,0.0)
move_target_flag = False
init_dist   = target.distance_from(start_loc)
#
#   Test to see if target specified is inside the boundary
#
target_loc = target.get_location()

if not boundary.check_inside(target_loc):
    print " Sorry, your target is not inside the current boundary "
    print " Current target  : " +str(target)
    print " Current boundary: " +str(boundary)
    print " Change target location or boundary size to correct problem"
    sys.exit(0)
#
#  Perform loop for each walk and collects statistics
# 
walk_steps = np.zeros(num_sim)  # Tracks number of steps for each walk
#   Execute main loop 'num_sim'  times 
for num in range(num_sim): 
    rand_walk = rw3d.RandomWalk3d(start_loc, max_steps, rand_function, boundary, target, move_target_flag)
    rand_walk.conduct_walk() 
    if rand_walk.get_target_hit():
        walk_steps[num] = rand_walk.get_num_steps()
    #
#   Print out key statistics and histogram of number of steps to ruin 
#
ave_step        = int(np.mean(walk_steps))
std_dev_steps   = int(np.std(walk_steps))
print 'Statistics for 3D walks with %d  simulations'  % num_sim
print '   Average number of steps to target is:  %d ' % ave_step
print '   Std deviation of number of steps  is:  %d ' % std_dev_steps   
print '   Largest number of steps to target is:  %d ' % int(np.max(walk_steps)) 
print 'Walk characteristics: '
print '   Boundary:', boundary
print '              Volume : %8.0f' % (boundary.volume())
print '   Target:', target
print '              Volume : %8.0f' % (target.volume())
print '   Starting point for walks : (%d,%d,%d) ' % (start_loc) 
print '   Distance from starting point to initial target = %5.2f' % (init_dist) 
print '   Move target flag is %s' % move_target_flag

#
#  Create histogram of steps to target for all simulations 
#
fig = plt.figure()
ax  = fig.add_subplot(1,1,1)  
ax.hist(walk_steps, bins=50, color='red')      
plt.title('Histogram of steps to target for 3D walks ' )
#  Place text with statistics on graph
ax.text(.75,.8, 'Ave steps: %d' %( ave_step), transform = ax.transAxes)
ax.text(.75,.75,'Std dev: %d' %( std_dev_steps),transform = ax.transAxes)
if move_target_flag:
    ax.text(.75,.70,'Target moves!!',transform = ax.transAxes)    
plt.grid(True)
#    plt.savefig("rw2d_hist.pdf") 
plt.show()

