
"""
  Classes to represent 3D closed shapes which can be used for confining
       boundary or intended target for a given random walk. Move and move 
       random methods can allow target to move during random walk

  Shape class is a super-class from which other base classes inherit methods.

  Classes available for closed shapes for boundary and target include:
           Rectangular Box
           Sphere
           Ellipsoid
           Polygon (future- not fully implemented yet)
"""  

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from itertools import product, combinations
import matplotlib.patches as patches

class Shape3d:
    """
    Super Class for all 3d shapes. Includes common methods for all shapes.
    """
    def __init__(self, location, rotation = 0 ):
        """
        Initializes the class object. Rotation is not implemented.
        """
        self._location = location
        self._init_location = location
        self._rotation = rotation 

    def get_location(self):
        """
        Returns current location (center) of shape
        """        
        return self._location

    def get_init_location(self):
        """
        Returns initial location (center) of shape
        """        
        return self._init_location

    def distance_from(self, point):
        """
        Returns distance from point to center of shape
        """ 
        center = self.get_location()
        x,y,z  = point
        return np.sqrt((x - center[0])**2 + (y - center[1])**2 + (z - center[2])**2)

    def move(self,new_location):
        """
        Moves the location of shape
        """
        self._location = new_location


    def move_random(self,rand_function,boundary):
        """
        Attempts random move of shape within larger shape (boundary)
        rand_function is the random function used to suggest move
        (eg.rand_angle or rand_grid). 'boundary' is the name of bounding shape 
        """
        # Create trial move
        xloc,yloc,zloc = self._location
        xdelta, ydelta, zdelta = rand_function()
        xtrial = xloc + xdelta
        ytrial = yloc + ydelta
        ztrial = zloc + zdelta
        # If move is inside boundary, execute move. Else, do nothing
        inside_boundary = boundary.check_inside((xtrial, ytrial,ztrial))
        if inside_boundary:      
            self.move((xtrial,ytrial,ztrial))


class Rectangle3d(Shape3d):
    """
    Class to represent rectanglar 3d shape
    """
    
    def __init__(self,location, width, height, depth, rotation = 0):
        """
        Initializes the Rectangle3d class object. Rotation is not implemented.
        """
#       super().__init__(location,rotation)  Python 3 syntax
        Shape3d.__init__(self,location,rotation)
        self._width    = width
        self._height   = height
        self._depth    = depth

    def __str__(self):
        """
        Creates printable output for rectangle3d object
        """        
        return "Rectanguar box with width = "+ str(self._width)+", height = "+ str(self._height)+",and depth = "+ str(self._depth) + "  centered at "+ str(self._init_location)

    def get_width(self):
        """
        Returns width of rectangle3d
        """      
        return self._width

    def get_height(self):
        """
        Returns height of rectangle3d
        """  
        return self._height

    def get_depth(self):
        """
        Returns height of rectangle3d
        """  
        return self._depth

    def volume(self):
        """
        Returns volume of shape
        """ 
        return self._width * self._height * self._depth 


   

    def get_bottom_left_corner(self):
        """
        Returns tuple of co-ordinates (x,y,z) of bottom left corner of rectangle
        """           
        xloc,yloc,zloc = self._location
        point = (xloc-.5 * self._width, yloc-.5* self._height,zloc-.5 * self._depth)
        return point

    def get_upper_right_corner(self):
        """
        Returns tuple of co-ordinates (x,y,z) of upper right corner of
        rectangle3d
        """       
        xloc,yloc,zloc = self._location
        point = (xloc + .5* self._width, yloc+.5 * self._height, zloc+.5 * self._depth) 
        return point

    def check_inside(self,point):
        """  
        Checks if point is inside a rectangle. Returns True
         if inside, False if not. Point is tuple (x,y,z) 
        """ 
        x,y,z = point
        xmin, ymin,zmin = self.get_bottom_left_corner()
        xmax, ymax,zmax = self.get_upper_right_corner()
        if (xmax>x and xmin<x) and (ymax>y and ymin<y) and (zmax> z and zmin< z):
            return True
        else:
            return False

    
    def draw_shape(self, ax, color='b', line_size=2.5):
        """
        Plots the rectangle3d shape using maplotlib plot3D 
        """
        #draw box
        xmin, ymin,zmin = self.get_bottom_left_corner()
        xmax, ymax,zmax = self.get_upper_right_corner()
        xdim = [xmin, xmax]
        ydim = [ymin, ymax]
        zdim = [zmin, zmax]
        corner_pts = np.array(list(product(xdim,ydim,zdim)))
        possible_edges   = combinations(corner_pts,2) 
        for pt1, pt2 in possible_edges:
            if ((pt1[0]==pt2[0] and pt1[1]==pt2[1]) or (pt1[0]==pt2[0] and pt1[2]==pt2[2]) or (pt1[1]==pt2[1] and pt1[2]==pt2[2])):
                ax.plot3D(*zip(pt1,pt2), c=color ,lw=line_size)
#  Note : alternate draw_shape command for solid surface
#         ax.plot_surface(tx, ty, tz, rstride=4, cstride=4, color=color)

    def set_plot_size(self,ax):
        """
        Sets plot size (limits) for boundary Rectangle
        """
        max_size = max(self.get_height(),self.get_width(),self.get_depth())
        ax.set_xlim3d([-max_size,max_size])
        ax.set_ylim3d([-max_size,max_size])
        ax.set_zlim3d([-max_size,max_size])


class Sphere(Shape3d):
    """
    Class to represent sphere shape
    """
    
    def __init__(self,location, radius):
        """
        Initializes the Circle class object. 
        """
        Shape3d.__init__(self,location)
        self._radius    = radius
       
    def __str__(self):
        """
        Creates printable output for shape
        """        
        return "Sphere with radius = "+ str(self._radius)+", centered at "+ str(self._init_location)
    
    def get_radius(self):
        """
        Returns radius of Circle
        """   
        return self._radius

    def volume(self):
        """
        Returns area of shape
        """ 
        return (4* np.pi * self._radius**3)/3.0 


    def check_inside(self,point):
        """  
        Checks if point is inside circle. Returns True
         if inside, False if not. Point is tuple (x,y) 
        """ 
        x,y,z = point
        xcenter, ycenter, zcenter = self.get_location()
        radius = self._radius
        if radius**2 > (x-xcenter)**2 + (y-ycenter)**2+ (z-zcenter)**2:
            return True
        else:
            return False

     
    def draw_shape(self, ax, color='r', line_size=2.5):
        """
        Plots the shape using maplotlib patches 
        """
        center = self.get_location()
        r = self._radius
        u, v = np.mgrid[0:2*np.pi:20j, 0:np.pi:10j]
        x=np.cos(u)*np.sin(v) * r + center[0]
        y=np.sin(u)*np.sin(v) * r + center[1]
        z=np.cos(v) * r  + center[2]
        ax.plot_wireframe(x, y, z, color=color,lw= line_size)
#  Note : alternate draw_shape command for solid surface
#         ax.plot_surface(x, y, z, rstride=4, cstride=4, color=color)
       

    def set_plot_size(self, ax):
        """
        Sets plot size (limits) for boundary
        """
        max_size = self.get_radius() 
        ax.set_xlim3d([-max_size,max_size])
        ax.set_ylim3d([-max_size,max_size])
        ax.set_zlim3d([-max_size,max_size])
#        xmax,ymax,zmax = xc+r, yc+r, zc+r 
#        xmin,ymin,zmin = xc-r, yc-r, zc-r
#        ax.set_xlim([xmin- r *.1, xmax + r *.1])
#        ax.set_ylim([ymin- r *.1, ymax + r *.1])
#        ax.set_zlim([zmin- r *.1, zmax + r *.1])           
# 
class Ellipsoid(Shape3d):
    """
    Class to represent ellipsoid shape. Lengths of semi-principal axes
    are a, b, and c, along x-axis, y axis, and z-axis respectively. 
    """
    
    def __init__(self,location, a, b, c, rotation = 0):
        """
        Initializes the Ellipse class object. Rotation is not implemented.
        """
        Shape3d.__init__(self,location,rotation)
        self._a    = a
        self._b    = b
        self._c    = c
        
    def __str__(self):
        """
        Creates printable output for shape
        """        
        return "Ellipsoid with a axis = "+ str(self._a)+", b axis = "+ str(self._b)+", and c axis = "+ str(self._c)+ "  centered at "+ str(self._init_location)

    def get_a(self):
        """
        Returns length of semi_principal axis a ( x orientation)
        """      
        return self._a

    def get_b(self):
        """
        Returns length of semi_principal axis b ( y orientation)
        """      
        return self._b

    def get_c(self):
        """
        Returns length of semi_principal axis c ( z orientation)
        """      
        return self._c

    def volume(self):
        """
        Returns volume of shape
        """ 
        return (4.0 * np.pi * self._a * self._b * self._c)/3.0
 

    def check_inside(self,point):
        """  
        Checks if point is inside shape. Returns True
         if inside, False if not. Point is tuple (x,y,z) 
        """ 
        x, y, z   = point
        xc, yc, zc = self.get_location()
        if (x-xc)**2/self._a**2 + (y-yc)**2/self._b**2+ (z-zc)**2/self._c**2 < 1.0:
            return True
        else:
            return False

 
    def draw_shape(self, ax, color='r', line_size=2.5):
        """
        Plots the shape using maplotlib wireframe surface 
        """
        # Get center and lengths of semi_principal axes (a, b, c)
        xc, yc, zc = self.get_location()
        a = self.get_a()
        b = self.get_b()
        c = self.get_c()
        # Use spherical angles to set grid co-ordinates:
        u, v = np.mgrid[0:2*np.pi:20j, 0:np.pi:10j]
        x= a * np.cos(u)*np.sin(v) + xc
        y= b * np.sin(u)*np.sin(v) + yc
        z= c * np.cos(v) + zc
        # Plot shape as transparent wireframe:
        ax.plot_wireframe(x, y, z, color=color,lw= line_size)

       

    def set_plot_size(self, ax):
        """
        Sets plot size (limits) for boundary
        """
        a = self.get_a()
        b = self.get_b()
        c = self.get_c()
        max_size = max(a, b, c)
        ax.set_xlim3d([-max_size,max_size])
        ax.set_ylim3d([-max_size,max_size])
        ax.set_zlim3d([-max_size,max_size])

