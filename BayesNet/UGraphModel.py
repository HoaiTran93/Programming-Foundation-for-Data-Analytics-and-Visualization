import numpy as np
import sys
from IGraph import IGraph
from AbstractGraph import *
from queue import PriorityQueue

class UGraphModel(AbstractGraph):
    def __init__(self):
        AbstractGraph.__init__(self)

    def connect(self, vFrom, vTo, weight=0):
        try:
            nodeF = self.getVertexNode(vFrom)
        except nodeF is None:
            msg = "The following vertex is not found: {}".format(vFrom)
            print(msg)

        try:
            nodeT = self.getVertexNode(vTo)
        except nodeT is None:
            msg = "The following vertex is not found: {}".format(vTo)
            print(msg)

        nodeF.connect(nodeT, weight)
        nodeT.connect(nodeF, weight)

    def disconnect(self, vFrom, vTo):
        try:
            nodeF = self.getVertexNode(vFrom)
        except nodeF is None:
            msg = "The following vertex is not found: {}".format(vFrom)
            print(msg)

        try:
            nodeT = self.getVertexNode(vTo)
        except nodeT is None:
            msg = "The following vertex is not found: {}".format(vTo)
            print(msg)
        
        try:
            edge = self.getEdge(nodeT)
        except edge is None:
            msg = "The following vertex is not found: {}".format(edge)
            print(msg)

        nodeF.removeTo(nodeT) #nodeF.inDegree -= 1; nodeF.outDegree -= 1;
        nodeT.removeTo(nodeF) #nodeT.inDegree -= 1; nodeT.outDegree -= 1;

    def remove(self, vertex):
        try:
            nodeF = self.getVertexNode(vertex)
        except nodeF is None:
            msg = "The following vertex is not found: {}".format(nodeF)
            print(msg)

        for nodeT in self.nodeList:
            edge = nodeF.getEdge(nodeT)
            if edge is not None:
                nodeF.removeTo(nodeT)
                nodeT.removeTo(nodeF)

        self.nodeList.remove(nodeF)

##
class UGraphModelAlgorithm(UGraphModel):
    def __init__(self, graph):
        self.graph = graph

    def minSpanningTree(self):
        ##//(1) Obtain the list ot vertices being processed
        vertexList = []
        vertexIt = self.graph.iterator()
        while vertexIt.hasNext():
            vertex = vertexIt.next()
            vertexList.append(vertex)
        print("vertexList:", vertexList)
        ##(2) Process each vertex in vertexList
        mst = UGraphModel()
        while vertexList:
            vertex = vertexList[0]
            vertexList.remove(vertex)

            mst.add(vertex)
            hasChildren = True

            while hasChildren:
                crossEdges = PriorityQueue()
                mstIt = mst.iterator()
                while mstIt.hasNext():
                    parent = mstIt.next()
                   # print("parent:",parent)
                    children = self.graph.getOutwardEdges(parent)

                    childrenIt = iter(children)
                    #print("child:", child)
                    while True:
                        child = next(childrenIt, None)
                        if child is None:
                            break
                        if not mst.contains(child):
                            weight = self.graph.getWeight(parent, child)
                            #print("weight:", weight)
                            msg = "parent:{}, child:{}, weight:{}".format(parent, child, weight)
                            print(msg)
                            edge = UGraphModelAlgorithm.Edge(parent, child, weight) ##to use inner class: inner = outer.Inner() . refer https://www.datacamp.com/community/tutorials/inner-classes-python
                            crossEdges.put(edge)

                hasChildren = crossEdges.qsize() > 0
                if hasChildren:
                    smallest = crossEdges.get()
                    msg = "smallest vFrom:{}, vTo:{}, weight:{}".format(smallest.vFrom, smallest.vTo, smallest.weight)
                    print(msg)
                    mst.add(smallest.vTo)
                    mst.connect(smallest.vFrom, smallest.vTo, smallest.weight)
                    vertexList.remove(smallest.vTo)

        return mst       

    ##inner class Egde
    class Edge():
        def __init__(self, vFrom, vTo, weight):
            self.vFrom = vFrom
            self.vTo = vTo
            self.weight = weight

        def __eq__(self, other):
            return self.weight == other.weight

        def __lt__(self, other):
            return self.weight < other.weight

        def __gt__(self, other):
            return self.weight > other.weight

    ##inner class Edge comparator
    class EdgeComparator(Edge):
        def __init__(self):
            return None

        def compare(self, o1, o2):
            diff = o1.weight - o2.weight
            if diff < 0:
                return -1
            elif diff > 0:
                return 1
            else:
                return 0

        
