import sys, getopt
from ReadInput import *
import time
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
    sample = 300000
    NodeList = [ rp.model.getVertexNode(nodeName).tableProb for nodeName in topo ]
    ListOutput = []
    for ques_index in range(len(Obser)):
        #Observations = { 'I' : 'Cao', 'D' : 'Kho' }
        if len(Obser[ques_index]) == 0:
            Observations = {}
        else:
            Observations = Obser[ques_index]
        print(Observations)
        Question     = Ques[ques_index]
        RunForwardList = []
        RunForwardWeight = []
        start_time = time.time()
        for sampleIndex in range(sample):
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
        
        NodeNameList = topo
    
        RunValueList = []
        WeightList = []
        KeyList = []
        for index_,RunForwardValue in enumerate(RunForwardList):
            OneRow = []
            for key in RunForwardValue: 
                if key not in Observations:
                    if index_ == 0:
                        KeyList.append(key)
                    OneRow.append(RunForwardValue[key])
            RunValueList.append(OneRow)
            WeightList.append(RunForwardWeight[index_])
        NumpyRunValue = np.array(RunValueList)
        NumpyKey = np.array(list(KeyList))
        NumpyWeight = np.array(WeightList)

        TotalWeight = np.sum(NumpyWeight)
        ListofIndexQues = []
        for Node in Question:
            print(NumpyKey)
            
            NodeName = Node
            Value    = Question[NodeName]
            print(NodeName)
            indexNumpyRunValue = np.where(NumpyKey==NodeName)[0][0]
            print(indexNumpyRunValue)
            ListofIndexQues += list(np.where(NumpyRunValue[:,indexNumpyRunValue] == Value)[0])
            print(len(list(np.where(NumpyRunValue[:,indexNumpyRunValue] == Value)[0])))

        print(len(ListofIndexQues))
        ListofIndexQues = list(set(ListofIndexQues))
        Output = np.sum(NumpyWeight[ListofIndexQues]) /TotalWeight
        ListOutput.append(Output)
        print("Sampling Time: ", (time.time()-start_time))

    OutputFile = open("output.txt","w") 
    for Output in ListOutput:
        OutputFile.writelines(str(round( Output, 2  ))+'\n')
    OutputFile.close()
if __name__ == "__main__":
    main(sys.argv[1:])    