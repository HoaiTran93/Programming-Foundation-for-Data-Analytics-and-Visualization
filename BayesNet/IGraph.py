import numpy as np
import sys

##
class IGraph():
    def __init__(self):
        pass
    
    def add(self, vertex):
        pass
    
    def remove(self, vertex):
        pass
    
    def contains(self, vertex):
        pass
       
    def connect(self, vFrom, vTo, weight=0):
        pass
    
    def disconnect(self, vFrom, vTo):
        pass
    
    def weight(self, vFrom, vTo):
        pass
    
    def getOutwardEdges(self, vFrom):
        pass
    
    def getInwardEdges(self, vFrom):
        pass
    
    def iterator(self):
        pass
    
    def size(self):
        pass
    
    def getVertexInDegree(self, vertex):
        pass
    
    def getVertexOutDegree(self, vertex):
        pass
    
    def println(self):
        pass
    
##
class Path():
    def __init__(self):
        self.path = []
        self.cost = 0
    
    def add(self, item):
        self.path.append(item)
        
    def toString(self):
        desc = '['
        it = iter(self.path)
        while True:
            item = next(it, None)
            if item is None:
                desc += ' ' + str(item)
                break
            desc += ' ' + str(item) + ','
        desc += ']'
        desc += ": {}".format(self.cost)
        return desc

##
class IFinder(IGraph):
    def __init__(self):
        pass
    def dijkstra(self, graph, start):
        pass
