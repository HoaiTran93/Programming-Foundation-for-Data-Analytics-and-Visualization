import numpy as np
import sys

class ConditionalProbabilityTable():
    def __init__(self,initTable,initParents,initNodeName):
        self.initTable = initTable
        TableShape = np.array(initTable).T.shape
        self.ProbabilityTable = np.array(initTable).T[:-1].reshape(TableShape[0]-1,TableShape[1])
        self.ProbabilityTableValues = np.array(initTable).T[-1].astype(np.float)
        self.ParentsList = initParents
        self.NodeName = initNodeName
        if self.isDiscreteDistribution() == False:
            self.ParentsNum = len(initParents)
            if self.ProbabilityTable.shape[0]-2 != self.ParentsNum:
                raise NameError("Init failed, number of parents is wrong!")

    def getValueList(self):
        return list(set(self.ProbabilityTable[-1]))

    def isDiscreteDistribution(self):
        if self.ParentsList == ['']:
            return True
        else:
            False

    def getNodeProbability(self,ParentState):
        RunTable = self.ProbabilityTable
        ValueTable = self.ProbabilityTableValues
        for name in self.ParentsList:
            if name in ParentState:
                State = np.array(ParentState[name])
                index = np.where( RunTable[0] == State )[0]
                RunTable = RunTable[1:,index] 
                ValueTable = ValueTable[index]
            else:
                raise NameError("Parents state is not enough")
        return RunTable[0], ValueTable

    def getOutput(self,ParentState):
        if self.isDiscreteDistribution(): 
            NodeProba = self.ProbabilityTable[0]
            ValueTable = self.ProbabilityTableValues
        else:
            NodeProba,ValueTable = self.getNodeProbability(ParentState)     
        RandomValue = np.random.random()
        for index in range(len(NodeProba)):
            if RandomValue < ValueTable[:index+1].sum():
                ParentState[self.NodeName] = NodeProba[index]
                return ParentState
        ParentState[self.NodeName] = NodeProba[-1]
        return ParentState

    def getOutputWithLikehood(self, ParentState, ParentLikelihoodWeight, Observations):
        if self.NodeName not in Observations.keys():
            if self.isDiscreteDistribution():   
                NodeProba = self.ProbabilityTable[0]
                ValueTable = self.ProbabilityTableValues
            else:
                NodeProba,ValueTable = self.getNodeProbability(ParentState)
            RandomValue = np.random.random()
            for index in range(len(NodeProba)):
                if RandomValue < ValueTable[:index+1].sum():
                    ParentState[self.NodeName] = NodeProba[index]    
                    return ParentState, ParentLikelihoodWeight
            ParentState[self.NodeName] = NodeProba[-1]
            return ParentState, ParentLikelihoodWeight
        else:
            if self.isDiscreteDistribution():   
                NodeProba = self.ProbabilityTable[0]
                ValueTable = self.ProbabilityTableValues
            else:
                NodeProba,ValueTable = self.getNodeProbability(ParentState)
            index = np.where(NodeProba==np.array(Observations[self.NodeName]))[0]
            ParentState[self.NodeName] = NodeProba[index]
            ParentLikelihoodWeight[self.NodeName] = float(ValueTable[index])
            return ParentState, ParentLikelihoodWeight

    def toString(self):
        desc = ''
        for i in range(len(self.initTable)):
            for j in range(len(self.initTable[i])):
                desc += str(self.initTable[i][j]) + " "
            desc += "\n"
        desc += str(self.ParentsList) + " " + str(self.NodeName)
        return desc
