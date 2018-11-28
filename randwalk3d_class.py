 
"""
  Module describes a class (RandomWalk3d)  of 3D random walks.
  Walks can be confined to an arbitrary boundary shape and seek out
  a target shape inside the boundary. Both are optional.

  Helper functions, rand_angle and rand_grid define selectable 
  functions for individual random moves.

  Possible boundary and target shapes are described in the 
  shapes_class.py module   
"""

import random
import numpy as np
import matplotlib.pyplot as plt
random.seed(None)        # Seed generator, None => system clock

def rand_grid():
    """  
    Performs unit 3D random step on an (x,y) grid 
    Returns one of : (1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),or (0,0,-1)  
    """
    x,y,z  = random.choice([(1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1)])
    return x, y, z

def rand_direct():
    """  
    Performs unit 3D random step in random direction on unit sphere
    Returns (x,y,z) co-ordinates of unit step at random direction
     """
    x,y,z = random.gauss(0,1), random.gauss(0,1), random.gauss(0,1)
    norm_factor = np.sqrt(x**2 + y**2 +z**2)
    x,y,z = x/norm_factor, y/norm_factor, z/norm_factor
    return x, y, z

class RandomWalk3d:
    """
    Class to represent a 3D random walk.
    Boundary shape defined by "boundary", target shape by "target" 
    walk is the sequence of random steps taken by walker
    """
    
    def __init__(self,start_loc, max_steps, rand_function, boundary= None,target = None, move_target=False ):
        """
        Initializes the RandomWalk3d class object:
            start_loc: starting location for walk
            max_steps: maximum number of steps that wlak will take
            rand     : random function to use for each step
            boundary : shape object describing the confining boundary for walk
            target   : shape object describing target for walk
            Note: boundary = None or target =None means boundary/target will not be
                  used for the walk (e.g walk is unconfined or has no target)
            move_target: False means target will remain at initial location during
                         walk, True means target will move randomly inside boundary 
            walk       : list which records step of random walk 
            num_steps  : number of steps required to reach target
            target_hit : True if target is reached during walk before maximum 
                         steps exceeded; False otherwise        
        """
        self._start_loc   = start_loc
        self._max_steps   = max_steps
        self._rand        = rand_function
        self._boundary    = boundary
        self._target      = target
        self._move_target = move_target
        self._walk        = []
        self._walk.append(start_loc)
        self._num_steps = 0 
        self._target_hit  = False 
 
    def get_start(self):
        """
        Returns starting point of the walk
        """        
        return self._start_loc

    def get_max_steps(self):
        """
        Returns maximum number of steps in walk. Walk stops if number exceeded,
        whether or not target is reached
        """     
        return self._max_steps

    def get_num_steps(self):
        """
        Returns total number of steps required to reach target for completed walk
        """    
        return self._num_steps

    def get_move_target(self):
        """
        Returns move_target selection (True if target moves during walk, 
        False if not)
        """    
        return self._move_target

    def get_target_hit(self):
        """
        Returns True if target is reached, False if not (and max_steps is
        exceeded during walk)
        """
        return self._target_hit

    def get_walk(self):
        """
        Returns list of all steps for completed walk, (x,y) tuple is recorded 
        for each step taken.
        """ 
        return self._walk

    def conduct_walk(self):
        """  
        Performs a random walk inside a boundary with target. 
        Walk proceeds until target is reached or max steps is exceeded 
        """
            
        xpos,ypos,zpos = self._start_loc
        while self._num_steps < self._max_steps :
            # Create trial move
            xdelta, ydelta, zdelta = self._rand()
            xtrial = xpos + xdelta
            ytrial = ypos + ydelta
            ztrial = zpos + zdelta
            #  If target exists, check if target reached. if so, end walk
            if self._target:
                inside_target = self._target.check_inside((xtrial, ytrial,ztrial))
                if inside_target:
                    xpos = xtrial
                    ypos = ytrial
                    zpos = ztrial
                    self._walk.append((xpos,ypos,zpos))
                    self._num_steps += 1
                    self._target_hit = True 
                    return
                elif self._move_target:
                    self._target.move_random(self._rand,self._boundary)

          
            # Check if still inside boundary. If so, accept move and continue 
            if self._boundary:
                inside_boundary = self._boundary.check_inside((xtrial, ytrial,ztrial))
                if inside_boundary:
                    xpos = xtrial
                    ypos = ytrial
                    zpos = ztrial
                    self._walk.append((xpos,ypos,zpos))
                    self._num_steps += 1
            else:   #  No boundary exists, carry on with walk
                xpos = xtrial
                ypos = ytrial
                zpos = ztrial
                self._walk.append((xpos,ypos,zpos))
                self._num_steps += 1           
            #  Max number of steps reached, without hitting target
        self._target_hit = False 
        return   
        

    def plot_walk(self, ax, line_type='r-',walk_num = 1, end_symbol='k*', end_size=10):
        """
        Plots the completed random walk on 2D graph using matplotlib objects 
        """
        
        xwalk = zip(*self._walk)[0]
        ywalk = zip(*self._walk)[1]
        zwalk = zip(*self._walk)[2]
        ax.plot(xwalk, ywalk,zwalk, line_type, label='rw'+str(walk_num)+' '+      \
                str(self._num_steps))
        # Large symbol ('k*') to mark end of walk       
        ax.plot([xwalk[-1]],[ywalk[-1]],[zwalk[-1]],end_symbol, ms= end_size)  
        # Large symbol (black dot: 'ko') to mark start of walk       
        ax.plot([xwalk[0]],[ywalk[0]],[zwalk[0]],'ko', ms= end_size)  
 


