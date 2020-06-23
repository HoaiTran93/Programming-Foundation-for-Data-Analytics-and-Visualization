import numpy as np
import sys
from UGraphModel import *
from DGraphModel import *
from TableProbility import *

class ReadModel():
    def __init__(self, inputName):
        self.file = open(inputName)
        self.model = DGraphModel()

    def generate(self):
        self.probMap = dict()
        #self.probValue = dict()
        for line in self.file:
            if len(line) == 2:
                self.numVertex = line.split('\n')[0]
            else:
                inputGraph = line.split('\n')[0]
                input = inputGraph.split(';')
                self.vertexName = input[0]
                #print("vertexName: ",vertexName)
                self.vertexParentName = input[1].split(',')
                #print("vertexParentName: ",self.vertexParentName)
                self.vertexes = input[2].split(',')
                #print("vertexes: ",self.vertexes)
                self.tableSize = input[3].split(',')
                #print("tableSize: ",self.tableSize)
                self.tableValue = input[4].split(',')
                #print("tableValue: ",self.tableValue)
                self.probMap.update({self.vertexName:self.vertexes})
                #self.probValue.update({self.vertexName:self.tableValue})
                self.init_graph()

    def parsing_tableProb(self):
        listProb = []
        for parent in (self.probMap[parentName] for parentName in self.vertexParentName if parentName != ''):
            #print("parent:",parent)
            listProb.append(parent)
        listProb.append(self.probMap[self.vertexName])
        #print("listProb: ", listProb)
        tableCombinationProb = self.parsing_combinationProb(listProb, self.tableValue)
        return tableCombinationProb

    def parsing_combinationProb(self, listProb, tableValue):
        #print("tableValue: ", tableValue)
        output = []
        n = len(listProb)
        total = 1
        for i in range(n):
            total *= len(listProb[i])
        index = np.zeros(n)
        index[-1] = -1

        count = 0
        while count < total:
            if index[n-1] != len(listProb[n-1]) - 1:
                index[n-1] += 1
            else:
                index[n-1] = 0
                preceding = n - 1
                while True:
                    preceding -= 1
                    if index[preceding] != len(listProb[preceding]) - 1:
                        index[preceding] += 1
                        break
                    else:
                        index[preceding] = 0
            aResult = []
            for i in range(n):
                aResult.append(listProb[i][int(index[i])])
            #print("count: ", count)
            aResult.append(float(tableValue[count]))
            output.append(aResult)
            count += 1
        #print(output)
        return output

    def init_graph(self):
        _tableProb = self.parsing_tableProb()
        self.tableProb = ConditionalProbabilityTable(_tableProb, self.vertexParentName, self.vertexName)
        self.model.add(self.vertexName, self.tableProb)
        for parent in self.vertexParentName:
            #print("parent: ",parent)
            if parent != '':
                self.model.connect(parent, self.vertexName)

class ReadTestCase():
    def __init__(self, inputName):
        self.file = open(inputName)

    def generate(self):
        listProb = []
        listObs = []
        for line in self.file:
            ObservationList = dict()
            Probability = dict()
            print("line: ",line)
            if len(line) == 2:
                numVertex = line.split('\n')[0]
            else:
                inputGraph = line.split('\n')[0]
                input = inputGraph.split(';')
                #print("input: ", input)
                prob = str(input[0])
                #print("prob: ", prob)
                for subProb in prob.split(','):
                    #print("subProb: ",subProb)
                    subP = subProb.split('=')
                    #print("subP: ", subP)
                    Probability.update({subP[0]:subP[1]})
                condition = input[1].split(',')
                #print("condition: ", condition)
                for subcondition in condition:
                    if subcondition == ' ':
                        ObservationList = []
                        break
                    sub = subcondition.split('=')
                    #print("subcondition: ",sub)
                    ObservationList.update({sub[0]:sub[1]})
                #print("Probability: ",Probability)
                #print("ObservationList: ",ObservationList)
                #print("=======")
                listProb.append(Probability)
                listObs.append(ObservationList)
        return listProb,listObs
        

    