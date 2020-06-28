import sys, getopt
from ReadInput import *
import time
import random
'''run directly'''
'''
def main():
    rp = ReadModel("input.txt")
    rp.generate()
    rp.model.println()
if __name__ == "__main__":
    main()
'''

'''run on console'''
def GetObserKey(Obser):
    KeyStr = ""
    if len(Obser) == 0:
        return "noobser"
    else:
        for key in  Obser:
            KeyStr += str(key)+Obser[key]
        return KeyStr

def main(argv):
    inputfile = ''
    testfile = ''
    opts, args = getopt.getopt(argv,"hi:i:",["model=","test="])
    for opt, arg in opts:
        if opt in ("--model"):
            inputfile = arg
        elif opt in ("--test"):
            testfile = arg
    rp = ReadModel(inputfile)
    rp.generate()
    rp.model.println()
    tp = ReadTestCase(testfile)
    Ques,Obser = tp.generate()
    print("a: ",Obser)
    print("b: ",Ques)
    
    DFS = 0
    BFS = 1
    sorter = TopoSorter(rp.model)
    topo = sorter.sort(BFS)
    print("topoBFS:", topo)
    
    print("TOPO", topo )
    LIKELIHOOD = True
    SAMPLE = 1000000
    NodeList = [ rp.model.getVertexNode(nodeName).tableProb for nodeName in topo ]
    ListOutput = []
    SamplingSetCache = {}
    if LIKELIHOOD == True:
        for ques_index in range(len(Obser)):
            random.seed(0)
            NodeNameList = topo
            if len(Obser[ques_index]) == 0:
                Observations = {}
            else:
                Observations = Obser[ques_index]
            print("Cache Key: ",GetObserKey(Observations))
            print("Observations: ",Observations)
            Question     = Ques[ques_index]

            if GetObserKey(Observations) not in SamplingSetCache:
                RunForwardList = []
                RunForwardWeight = []
                start_time = time.time()
                for _ in range(SAMPLE):
                    RunningVar = {}
                    ParentLikelihoodWeight = {}
                    w = 1
                    for nodeName in topo:   
                        node = rp.model.getVertexNode(nodeName)
                        RunningVar,ParentLikelihoodWeight = node.tableProb.getOutputWithLikehood(RunningVar,ParentLikelihoodWeight,Observations)
                    for key in Observations:
                        w *= ParentLikelihoodWeight[key]
                    RunForwardWeight.append(w)
                    RunForwardList.append(RunningVar)
                print("Sampling Time: ", (time.time()-start_time))
                
                RunValueList = []
                WeightList = RunForwardWeight
                KeyList = list(RunForwardList[0].keys())
                for index_,RunForwardValue in enumerate(RunForwardList):
                    RunValueList.append(list(RunForwardValue.values()))

                NumpyRunValue = np.array(RunValueList)
                NumpyKey = np.array(list(KeyList))
                NumpyWeight = np.array(WeightList)
                TotalWeight = np.sum(NumpyWeight)
                SamplingSetCache[GetObserKey(Observations)] = (NumpyRunValue, NumpyKey, NumpyWeight, TotalWeight)

            else:
                print("No need sampling agian!")
                NumpyRunValue, NumpyKey, NumpyWeight, TotalWeight = SamplingSetCache[GetObserKey(Observations)]



            ListofIndexQues = []
            for Node in Question:
                NodeName = Node
                Value    = Question[NodeName]
                indexNumpyRunValue = np.where(NumpyKey==NodeName)[0][0]
                ListofIndexQues += list(np.where(NumpyRunValue[:,indexNumpyRunValue] == Value)[0])

            ListofIndexQues = list(set(ListofIndexQues))
            Output = np.sum(NumpyWeight[ListofIndexQues]) /TotalWeight
            ListOutput.append(Output)
    else:
        # forward
        RunForwardList = []
        start_time = time.time()
        for _ in range(SAMPLE):
            RunningVar = {}
            for nodeName in topo:   
                node = rp.model.getVertexNode(nodeName)
                RunningVar = node.tableProb.getOutput(RunningVar)
            RunForwardList.append(RunningVar)
        
        print("Sampling Time: ", (time.time()-start_time))

        NodeNameList = topo
        for ques_index in range(len(Obser)):
            if len(Obser[ques_index]) == 0:
                Observations = {}
            else:
                Observations = Obser[ques_index]
            print(Observations)
            Question     = Ques[ques_index]

            RunValueList = []
            KeyList = RunForwardList[0].keys()
            for RunForwardValue in RunForwardList:
                OneRow = []
                ObservationsCheck = True
                for key in Observations:
                    if Observations[key] != RunForwardValue[key]:
                        ObservationsCheck = False
                if ObservationsCheck == True:
                    for key in RunForwardValue: 
                        OneRow.append(RunForwardValue[key])
                    RunValueList.append(OneRow)

            NumpyRunValue = np.array(RunValueList)
            NumpyKey = np.array(list(KeyList))

            TempObserMatrix = NumpyRunValue 
            for Node in Question:
                NodeName = Node
                Value    = Question[NodeName]
                indexNumpyRunValue = np.where(NumpyKey==NodeName)[0][0]
                indexQuers = np.where(TempObserMatrix[:,indexNumpyRunValue] == Value)[0]
                TempObserMatrix = TempObserMatrix[indexQuers]

            Output = len(np.where(NumpyRunValue[:,indexNumpyRunValue] == Value)[0])/NumpyRunValue.shape[0]
            print('============================')
            ListOutput.append(Output)


    OutputFile = open("output.txt","w") 
    for Output in ListOutput:
        print(Output)
        OutputFile.writelines(str( Output )+'\n')
    OutputFile.close()
if __name__ == "__main__":
    main(sys.argv[1:])    