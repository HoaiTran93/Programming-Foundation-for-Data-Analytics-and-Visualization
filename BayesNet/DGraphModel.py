import numpy as np
import sys
from IGraph import IGraph
from AbstractGraph import *

class DGraphModel(AbstractGraph):
    def __init__(self):
        AbstractGraph.__init__(self)

    def connect(self, vFrom, vTo, weight=0):
        nodeF = self.getVertexNode(vFrom)
        if nodeF is None:
            msg = "The following vertex is not found: {}".format(vFrom)
            raise Exception(msg)

        nodeT = self.getVertexNode(vTo)
        if nodeT is None:
            msg = "The following vertex is not found: {}".format(nodeT)
            raise Exception(msg)

        nodeF.connect(nodeT, weight)

    def disconnect(self, vFrom, vTo):
        nodeF = self.getVertexNode(vFrom)
        if nodeF is None:
            msg = "The following vertex is not found: {}".format(vFrom)
            raise Exception(msg)

        nodeT = self.getVertexNode(vTo)
        if nodeT is None:
            msg = "The following vertex is not found: {}".format(nodeT)
            raise Exception(msg)

        edge = self.getEdge(nodeT)
        if edge is None:
            msg = "Opps! E(from:{}, to:{})".format(vFrom, vTo)
            raise Exception(msg)
        
        nodeF.removeTo(nodeT)

    def remove(self, vertex):
        nodeA = self.getVertexNode(vertex)
        if nodeA is None:
            msg = "The following vertex is not found: {}".format(vertex)
            raise Exception(msg)

        #disconnect all
        for nodeB in self.nodeList:
            edge = nodeB.getEdge(nodeA)
            if edge is not None:
                nodeB.removeTo(nodeA)
            edge = nodeA.getEdge(nodeB)
            if edge is not None:
                nodeA.removeTo(nodeB)

        #remove
        self.nodeList.remove(nodeA)

##
class Stack():
    def __init__(self):
        self.sList = []

    def push(self, item):
        self.sList.insert(0, item)

    def pop(self):
        item = self.sList.pop(0)
        return item

    def peek(self):
        item = self.sList[0]
        return item

    def remove(self, item):
        return self.sList.remove(item)

    def contains(self, item):
        return (item in self.sList)

    def isEmpty(self):
        return (not self.sList)

    def size(self):
        return len(self.sList)

##
class Queue():
    def __init__(self):
        self.qList = []

    def push(self, item):
        self.qList.append(item)

    def pop(self):
        item = self.qList.pop(0)
        return item

    def peek(self):
        item = self.qList[0]
        return item

    def contains(self, item):
        return (item in self.qList)

    def isEmpty(self):
        return (not self.qList)

    def size(self):
        return len(self.qList)

##
class TopoSorter(Queue, Stack):
    def __init__(self, graph):
        Queue.__init__(self)
        Stack.__init__(self)
        self.graph = graph
        self.DFS = 0
        self.BFS = 1

    def sort(self, mode):
        if mode == self.DFS:
            return self.dfsSort()
        else:
            return self.bfsSort()

    def bfsSort(self):
        topoOrder = []
        indegreeMap = self.vertex2inDegree()
        bfsList = self.listOfZeroInDegrees()

        bfsQueue = Queue()
        for item in bfsList:
            bfsQueue.push(item)

        while bfsQueue.isEmpty() is not True:
            vertex = bfsQueue.pop()
            topoOrder.append(vertex)
            ##dec indegree of neighbors
            neighbors = self.graph.getOutwardEdges(vertex)
            for v in neighbors:
                prevDegree = indegreeMap[v]
                indegreeMap.update({v:prevDegree-1})
                if prevDegree == 1:
                    bfsQueue.push(v)

        return topoOrder

    def dfsSort(self):
        topoOrder = []
        outdegreeMap = self.vertex2outDegree()
        dfsList = self.listOfZeroInDegrees()

        dfsStack = Stack()
        for item in dfsList:
            dfsStack.push(item)

        while not dfsStack.isEmpty():
            vertex = dfsStack.peek()
            outDegree = outdegreeMap.get(vertex)
            if outDegree == 0:
                dfsStack.pop()
                topoOrder.insert(0, vertex)
            else:
                neighbors = self.graph.getOutwardEdges(vertex)
                for v in neighbors:
                    if dfsStack.contains(v):
                        dfsStack.remove(v)
                        dfsStack.push(v)
                    if not dfsStack.contains(v) and not v in topoOrder:
                        dfsStack.push(v)
                    outdegreeMap.update({vertex:outDegree - 1})
        ##while: stack not empty
        return topoOrder

    def vertex2inDegree(self):
        map = dict()
        vertexIt = self.graph.iterator()

        while vertexIt.hasNext():
            vertex = vertexIt.next()
            gInDegree = self.graph.getVertexInDegree(vertex)
            map.update({vertex:gInDegree})

        return map

    def vertex2outDegree(self):
        map = dict()
        vertexIt = self.graph.iterator()
        while vertexIt.hasNext():
            vertex = vertexIt.next()
            gOutDegree = self.graph.getVertexOutDegree(vertex)
            map.update({vertex:gOutDegree})

        return map

    def listOfZeroInDegrees(self):
        zList = []
        vertexIt = self.graph.iterator()
        while vertexIt.hasNext():
            vertex = vertexIt.next()
            inDegree = self.graph.getVertexInDegree(vertex)
            if inDegree == 0:
                zList.append(vertex)

        return zList