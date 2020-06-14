import numpy as np
import sys
from IGraph import IGraph
import pandas as pd
##
class Table():
    def __init__(self):
        self.tableProb = None
        return None

    def get(self):
        return self.tableProb

    def toString(self):
        return self.tableProb.to_string()

    def read_data(self, file_name):
        path = "./Data/" + str(file_name)
        data = pd.read_csv(path)
        self.tableProb = pd.DataFrame(data)
        return self.tableProb

##
class Edge():
    def __init__(self, vFrom, vTo, weight=None):
        self.vFrom = vFrom
        self.vTo = vTo
        self.weight = weight

    def equals(self, newEdge):
        fromEquality = (self.vFrom.vertex == newEdge.vFrom.vertex)
        toEquality = (self.vTo.vertex == newEdge.vTo.vertex)
        return fromEquality & toEquality

    def toString(self):
        desc = "E(from:{}, to:{})".format(self.vFrom, self.vTo)
        return desc

##
class VertexNode(Edge, Table):
    def __init__(self, data=None, tableProb = None):
        self.vertex = data
        self.tableProb = tableProb
        self.inDegree = self.outDegree = 0
        self.adList = []     
        
    def connect(self, vTo, weight):
        edge = self.getEdge(vTo)
        if edge is None:
            edge = Edge(self, vTo, weight) 
            self.adList.append(edge)
            edge.vFrom.outDegree += 1
            edge.vTo.inDegree += 1
        else:
            edge.weight = weight
            
    def getOutwardEdges(self):
        listNode = []
        it = iter(self.adList)
        while True:
            item = next(it, None)
            if item is None:
                break
            to = item.vTo.vertex
            listNode.append(to)
        return listNode
    
    def getEdge(self, vTo):
        edgeIt = iter(self.adList)
        while True:
            edge = next(edgeIt, None)
            if edge is None:
                break
            if edge.equals(Edge(self, vTo)):
                return edge
        return None

    def getTableProb(self):
        return self.tableProb

    def removeTo(self, vTo):
        edgeIt = iter(self.adList)
        while True:
            edge = next(edgeIt, None)
            if edge is None:
                break
            #if edge.vTo.vertex.equals(vTo.vertex): ==> python doesn't support Object.equals
            if edge.vTo.vertex == vTo.vertex:
                #edgeIt.remove() ==> iter python doesn't sp remove. refer to https://sopython.com/canon/95/removing-items-from-a-list-while-iterating-over-the-list/
                self.adList.remove(edge)
                edge.vFrom.outDegree -= 1
                edge.vTo.inDegree -= 1
                break
    
    def getInDegree(self):
        return self.inDegree

    def getOutDegree(self):
        return self.outDegree

    def toString(self):
        desc = "V({}, in:{}, out:{})".format(self.vertex, self.inDegree, self.outDegree)
        desc += "\n"
        desc += self.tableProb.toString()
        return desc

##
class GraphIterator():
    def __init__(self, graph, nodeIt):
        self.graph = graph
        self.nodeIt = nodeIt
        self.node = None
        self.afterMove = False
        self._hasNext = None

    def hasNext(self):
        if self._hasNext is None:
            try:
                self.theNext = next(self.nodeIt)
            except StopIteration:
                self._hasNext = False
            else:
                self._hasNext = True
        return self._hasNext
    
    def next(self):
        if self._hasNext:
            self.node = self.theNext
            self.afterMove = True
        else:
            self.node = next(self.nodeIt)
        self._hasNext = None
        return self.node.vertex

    def remove(self):
        if self.afterMove is True:
            self.graph.remove(self.node.vertex)
            self.afterMove = False

##
class AbstractGraph(IGraph, VertexNode, GraphIterator):
    def __init__(self):
        VertexNode.__init__(self)
        self.nodeList = []
        
    def getVertexNode(self, vertex):
        it = iter(self.nodeList)
        while True:
            node = next(it, None)
            if node is None:
                break
            if node.vertex == vertex: 
                return node
        return None
    
    def add(self, vertex, tableProb):
        self.nodeList.append(VertexNode(vertex, tableProb))

    def connect(self, vFrom, vTo, weight):
        VertexNode.connect(vFrom, vTo, weight)

    def contains(self, vertex):
        node = self.getVertexNode(vertex)
        return node != None

    def getWeight(self, vFrom, vTo):
        try:
            nodeF = self.getVertexNode(vFrom)
        except nodeF is None:
            msg = "The following vertex is not found: {}".format(vFrom)
            print(msg)

        try:
            nodeT = self.getVertexNode(vTo)
        except nodeT is None:
            msg = "The following vertex is not found: {}".format(vFrom)
            print(msg)
        
        try:
            edge = nodeF.getEdge(nodeT)
        except edge is None:
            msg = "Oops! That was no valid number. E(from:{}, to:{})".format(self.vFrom, self.vTo)
            print(msg)
        return edge.weight

    def getOutwardEdges(self, vFrom):
        try:
            node = self.getVertexNode(vFrom)
        except node is None:
            msg = "The following vertex is not found: {}".format(vFrom)
            print(msg)
        return node.getOutwardEdges()

    def getInwardEdges(self, vTo):
        listVertex = []
        nodeIt = iter(self.nodeList)

        while True:
            node = next(nodeIt, None)
            if node is None:
                break
            edgeIt = iter(node.adList)
            while True:
                edge = next(edgeIt, None)
                if edge is None:
                    break
                if edge.vTo.vertex == vTo:
                    listVertex.append(edge.vFrom.vertex)
        return listVertex

    def size(self):
        return len(self.nodeList)

    def getVertexInDegree(self, vertex):
        try:
            node = self.getVertexNode(vertex)
        except node is None:
            msg = "The following vertex is not found: {}".format(vertex)
            print(msg)
        return node.getInDegree()

    def getVertexOutDegree(self, vertex):
        try:
            node = self.getVertexNode(vertex)
        except node is None:
            msg = "The following vertex is not found: {}".format(vertex)
            print(msg)
        return node.getOutDegree()

    def println(self):
        print(self.toString())

    def toString(self):
        desc = "=======================================================\n"
        desc += "Vertices:\n"
        nodeIt = iter(self.nodeList)
        while True:
            node = next(nodeIt, None)
            if node is None:
                break
            desc += " " + node.toString() + "\n"
        
        desc += "------------------------------------------------------\n"
        desc += "Edges:\n"

        nodeIt = iter(self.nodeList)
        while True:
            node = next(nodeIt, None)
            if node is None:
                break
            edgeIt = iter(node.adList)
            #print(*node.adList, sep = ", ")
            while True:
                edge = next(edgeIt, None)
                if edge is None:
                    break
                line = "E({}, {}, {})".format(node.vertex, edge.vTo.vertex, edge.weight)
                desc += " " + line + "\n"
        
        desc += "======================================================\n"
        return desc

    def iterator(self):
        return GraphIterator(self, iter(self.nodeList))