import numpy as np
import sys

class ConditionalProbabilityTable():
    def __init__(self,initTable,initOrderProb,initParents,initNodeName):
        self.initTable = initTable
        self.ProbabilityTable = np.array(initTable).T.astype(dtype='<U21')
        self.OrderProb = initOrderProb
        self.ParentsList = initParents
        self.NodeName = initNodeName
        if self.isDiscreteDistribution() == False:
            self.ParentsNum = len(initParents)
            if self.ProbabilityTable.shape[0]-2 != self.ParentsNum:
                raise Exception("Init failed, number of parents is wrong!")

    def getValueList(self):
        return list(set(self.ProbabilityTable[-2]))

    def isDiscreteDistribution(self):
        if self.ParentsList == ['']:
            return True
        else:
            False

    def getNodeProbability(self,ParentState):
        RunTable = self.ProbabilityTable
        for name in self.ParentsList:
            if name in ParentState:
                State = np.array(ParentState[name]).astype(dtype='<U21')
                index = np.where( RunTable[0] == State )[0]
                RunTable = RunTable[1:,index]
            else:
                raise Exception("Parents state is not enough")
        return RunTable

    def getOutput(self,ParentState):
        if self.isDiscreteDistribution():
            sortedProba = self.ProbabilityTable.T[self.ProbabilityTable[1].argsort()].T
            #print("sortedProba1: ",sortedProba)
        else:
            NodeProba = self.getNodeProbability(ParentState)
            #print("NodeProba: ",NodeProba)
            sortedProba = NodeProba.T[NodeProba[1].argsort()].T
            #print("sortedProba2: ",sortedProba) 
        RandomValue = np.random.random()
        for index in range(len(sortedProba)):
            if RandomValue < sortedProba[1][:index+1].astype(np.float).sum():
                ParentState[self.NodeName] = sortedProba[0,index]
                #print("ParentState1: ", ParentState)
                return ParentState
        ParentState[self.NodeName] = sortedProba[0,-1]
        #print("ParentState2: ", ParentState)
        return ParentState


    def getOutputWithLikehood(self, ParentState, ParentLikelihoodWeight, Observations):
        if self.NodeName not in Observations.keys():
            if self.isDiscreteDistribution():
                sortedProba = self.ProbabilityTable.T[self.ProbabilityTable[1].argsort()].T
            else:
                NodeProba = self.getNodeProbability(ParentState)
                sortedProba = NodeProba.T[NodeProba[1].argsort()].T
            RandomValue = np.random.random()
            for index in range(len(sortedProba)):
                if RandomValue < sortedProba[1][:index+1].astype(np.float).sum():
                    ParentState[self.NodeName] = sortedProba[0,index]
                    return ParentState, ParentLikelihoodWeight
            ParentState[self.NodeName] = sortedProba[0,-1]
            return ParentState, ParentLikelihoodWeight
        else:
            if self.isDiscreteDistribution():
                sortedProba = self.ProbabilityTable.T[self.ProbabilityTable[1].argsort()].T
            else:
                NodeProba = self.getNodeProbability(ParentState)
                sortedProba = NodeProba.T[NodeProba[1].argsort()].T
            index = np.where(sortedProba[0]==np.array(Observations[self.NodeName]).astype(dtype='<U21'))[0][0]
            ParentState[self.NodeName] = sortedProba[0,index]
            ParentLikelihoodWeight[self.NodeName] = float(sortedProba[1,index])
            return ParentState, ParentLikelihoodWeight

    def toString(self):
        desc = ''
        for i in range(len(self.initTable)):
            for j in range(len(self.initTable[i])):
                desc += str(self.initTable[i][j]) + " "
            desc += "\n"
        desc += str(self.OrderProb)
        return desc
