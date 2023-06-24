'''Defines the QuadTree class used to group data into QuadTree Tree data structure'''
#Implemented with the aid of: https://www.youtube.com/watch?v=RKODYaueSvw
#import numpy as np

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Rectangle:
    def __init__(self, corner, width, height): #defines a rectangle given its bottom left corner, his width and his height
        self.corner = corner #a Point class object
        self.width = width
        self.height = height

        #defines boundaries of the Rectangle
        self.left = corner.x
        self.top = corner.y + height
        self.right = corner.x + width
        self.bottom = corner.y

    def ContainsData(self, data):
        '''checks for the data properties x and y return the binary value of the condition involving Rectangle class
        parameters'''
        return (self.left <= data.x < self.right and self.bottom <= data.y < self.top) 

    def draw(self, ax, c = 'k', lw = 1, alpha = 1, **kwargs):
        x1, y1 = self.left, self.bottom
        x2, y2 = self.right, self.top
        ax.plot([x1, x1, x2, x2, x1],[y1, y2, y2, y1, y1], c = c, lw = lw, **kwargs)

class TreeNode:
    def __init__(self, boundaries, capacity = 1): #capacity argument is just for testing
        self.boundaries = boundaries
        self.capacity = capacity

        self.StoredData = []
        self.divided = False #checks if the current node has been already divided

    def insert(self, data):
        #checks if the data is in the boundaries (rectangle of given width and height from its corner), all the 
        #binary values are assigned to know which QuadTree the given data below
        if not self.boundaries.ContainsData(data):
            return False
        
        #checks if the Node is avaliable for storing data
        if len(self.StoredData) < self.capacity:
            self.StoredData.append(data)
            return True
        
        if not self.divided:
            self.divide()

        if self.nw.insert(data):
            return True
        elif self.ne.insert(data):
            return True
        elif self.se.insert(data):
            return True
        elif self.sw.insert(data):
            return True
        
        #if for any reason the point is not added to any QuadTree
        return False

    def divide(self):
        x_corner = self.boundaries.corner.x
        y_corner = self.boundaries.corner.y
        new_width = 0.5*self.boundaries.width
        new_height = 0.5*self.boundaries.height

        #define childs
        nw = Rectangle(Point(x_corner, y_corner + new_height), new_width, new_height)
        self.nw = TreeNode(nw)
        
        ne = Rectangle(Point(x_corner + new_width, y_corner + new_height), new_width, new_height)
        self.ne = TreeNode(ne)
        
        se = Rectangle(Point(x_corner + new_width, y_corner), new_width, new_height)
        self.se = TreeNode(se)
        
        sw = Rectangle(Point(x_corner, y_corner), new_width, new_height)
        self.sw = TreeNode(sw)
        
        self.divided = True

    def __len__(self):
        count = len(self.StoredData)
        if self.divided:
            count += len(self.nw) + len(self.ne) + len(self.se) + len(self.sw)

        return count
    
    def draw(self, ax, c = 'k', lw = 1, alpha = 1):
        self.boundaries.draw(ax, c = c, lw = lw, alpha = alpha)

        if self.divided:
            self.nw.draw(ax, c = c, lw = lw, alpha = alpha)
            self.ne.draw(ax, c = c, lw = lw, alpha = alpha)
            self.se.draw(ax, c = c, lw = lw, alpha = alpha)
            self.sw.draw(ax, c = c, lw = lw, alpha = alpha)