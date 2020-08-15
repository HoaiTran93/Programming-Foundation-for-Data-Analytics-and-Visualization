import numpy as np
import sys
from UGraphModel import *
from DGraphModel import *
from TableProbility import *

class ReadModel():
    def __init__(self, inputName):
        self.file = open(inputName)
        self.model = DGraphModel()

    def correctInput(self):
        lines = self.file.readlines()

        ##remove spaces##
        for i in range(len(lines)):
            lines[i] = lines[i].strip()
            lines[i] = lines[i].replace(' ','')

        ##remove empty lines##
        while lines.count('') > 0:
            lines.remove('')
        
        self.lines = lines

    def generate(self):
        self.correctInput()
        self.probMap = dict()
        #self.probValue = dict()
        for line in self.lines:
            if line.find(";") == -1: #check num vertex
                self.numVertex = int(line)
                #print("numVertex: ",self.numVertex)
                if self.numVertex != len(self.lines) - 1:
                    raise Exception("Num vertex is not enough")
            else:
                input = line.split(';')
                #print("input: ",input)
                self.vertexName = input[0]
                #print("vertexName: ",self.vertexName)
                self.vertexParentName = input[1].split(',')
                # print("vertexParentName: ",self.vertexParentName)
                self.vertexes = input[2].split(',')
                # print("vertexes: ",self.vertexes)
                self.tableSize = input[3].split(',')
                # print("tableSize: ",self.tableSize)
                self.tableValue = input[4].split(',')
                # print("tableValue: ",self.tableValue)
                self.probMap.update({self.vertexName:self.vertexes})
                #self.probValue.update({self.vertexName:self.tableValue})
                self.init_graph()

    def parsing_tableProb(self):
        listProb = []
        #print("vertexParentName: ",self.vertexParentName)
        order_Prob = []
        for parent in (self.probMap[parentName] for parentName in self.vertexParentName if parentName != ''):
            # print("parent:",parent)
            listProb.append(parent)
        listProb.append(self.probMap[self.vertexName])
        # print("listProb: ", listProb)
        tableCombinationProb = self.parsing_combinationProb(listProb, self.tableValue)
        if self.vertexParentName != ['']: 
            for index in range(len(self.vertexParentName)):
                #print("item: ", self.vertexParentName[index])
                order_Prob.append(self.vertexParentName[index])
        order_Prob.append(self.vertexName)
        #print("listnode: ", order_Prob)
        return tableCombinationProb, order_Prob

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
        _tableProb,_orderProb = self.parsing_tableProb()
        self.tableProb = ConditionalProbabilityTable(_tableProb, _orderProb, self.vertexParentName, self.vertexName)
        self.model.add(self.vertexName, self.tableProb)
        for parent in self.vertexParentName:
            #print("parent: ",parent)
            if parent != '':
                self.model.connect(parent, self.vertexName)

class ReadTestCase():
    def __init__(self, inputName):
        self.file = open(inputName)

    def correctInput(self):
        lines = self.file.readlines()

        ##remove spaces##
        for i in range(len(lines)):
            lines[i] = lines[i].strip()
            lines[i] = lines[i].replace(' ','')

        ##remove empty lines##
        while lines.count('') > 0:
            lines.remove('')
        
        self.lines = lines
        
    def generate(self):
        self.correctInput()
        listConditions = []
        listObservations = []

        for line in self.lines:
            Observation = dict()
            Condition = dict()
            done_parse = False
            #print("line: ",line)
            if line.find(";") == -1: #check numtest case
                self.numTestcase = int(line)
                #print("numTestcase: ",self.numTestcase)
                if self.numTestcase != len(self.lines) - 1:
                    raise Exception("Num testcase is not enough")
            else:
                input = line.split(';')
                #print("input: ", input)
                prob = str(input[0])
                if prob.find("=") == -1: # check exactly approxiate
                    Obser = prob.split(',')
                    Condit = input[1].split(',')
                    listConditions.append(Condit)
                    listObservations.append(Obser)
                    done_parse = True
                else:
                    #print("prob: ", prob)
                    for subProb in prob.split(','):
                        #print("subProb: ",subProb)
                        subP = subProb.split('=')
                        #print("subP: ", subP)
                        Observation.update({subP[0]:subP[1]})
                if not done_parse:
                    condition = input[1].split(',')
                    #print("condition: ", condition)
                    for subcondition in condition:
                        if subcondition == '':
                            Condition = []
                            break
                        sub = subcondition.split('=')
                        #print("subcondition: ",sub)
                        Condition.update({sub[0]:sub[1]})
                    #print("Probability: ",Probability)
                    #print("ObservationList: ",ObservationList)
                    #print("=======")
                    listConditions.append(Condition)
                    listObservations.append(Observation)
        return listObservations, listConditions
        

    