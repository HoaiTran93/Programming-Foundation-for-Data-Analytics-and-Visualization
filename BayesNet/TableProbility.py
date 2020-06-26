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
        self.SortTable , self.SortValues =  self.SortMax2MinProb( self.ProbabilityTable[0] , self.ProbabilityTableValues )
        if self.isDiscreteDistribution() == False:
            AllParentsKey = np.unique(np.array(initTable)[:,:-2],axis=0)
            self.DictofMinTable = {}
            for i in range(AllParentsKey.shape[0]):
                QueryDict = {}
                KeyDict   = ""
                for j in range(AllParentsKey.shape[1]):
                    QueryDict[self.ParentsList[j]] = AllParentsKey[i,j]
                    KeyDict += self.ParentsList[j]+str(AllParentsKey[i,j])
                self.DictofMinTable[KeyDict] =  self.getNodeProbability(QueryDict)

            self.ParentsNum = len(initParents)
            if self.ProbabilityTable.shape[0]-1 != self.ParentsNum:
                raise NameError("Init failed, number of parents is wrong!")
        
    def getValueList(self):
        return list(set(self.ProbabilityTable[-1]))

    def isDiscreteDistribution(self):
        if len(self.ParentsList) ==  1 and self.ParentsList[0] == "":
            return True
        else:
            return False
    
    def SortMax2MinProb(self,RunTable,ValueTable):
        SortMax2MinIndex = ValueTable.argsort()[::-1]
        return RunTable[SortMax2MinIndex], ValueTable[SortMax2MinIndex]
    
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
            
        return self.SortMax2MinProb ( RunTable[0], ValueTable )
    
    def getNodeProbabilityImmediately(self,ParentState):
        KeyDict = ""
        for name in self.ParentsList:
            if name in ParentState:
                KeyDict += name+str(ParentState[name])
            else:
                raise NameError("Parents state is not enough")
        return self.DictofMinTable[KeyDict]
    
    def getOutput(self,ParentState):
        if self.isDiscreteDistribution(): 
            NodeProba,ValueTable = self.SortTable , self.SortValues
        else:
            NodeProba,ValueTable = self.getNodeProbabilityImmediately(ParentState)     
            
        RandomValue = np.random.random()
        ProbThreshold = 0
        for index in range(len(NodeProba)):
            ProbThreshold += ValueTable[index]
            if RandomValue < ProbThreshold:
                ParentState[self.NodeName] = NodeProba[index]
                return ParentState
        
    def getOutputWithLikehood(self, ParentState, ParentLikelihoodWeight, Observations):
        if self.NodeName not in Observations.keys():
            if self.isDiscreteDistribution():   
                NodeProba,ValueTable = self.SortTable , self.SortValues
            else:
                NodeProba,ValueTable = self.getNodeProbabilityImmediately(ParentState)
            # Sampling
            RandomValue = np.random.random()
            ProbThreshold = 0
            for index in range(len(NodeProba)):
                ProbThreshold += ValueTable[index]
                if RandomValue < ProbThreshold:
                    ParentState[self.NodeName] = NodeProba[index]    
                    return ParentState, ParentLikelihoodWeight
        else:
            
            if self.isDiscreteDistribution():   
                NodeProba, ValueTable = self.SortTable , self.SortValues
            else:
                NodeProba,ValueTable = self.getNodeProbabilityImmediately(ParentState)
            # No need sampling    
            for index in range(len(NodeProba)):
                if NodeProba[index] == Observations[self.NodeName]:
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
