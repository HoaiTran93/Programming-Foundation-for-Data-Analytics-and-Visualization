import sys, getopt
from ReadInput import *

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
    a,b = tp.generate()
    print("a: ",a)
    print("b: ",b)

    DFS = 0
    BFS = 1
    sorter = TopoSorter(rp.model)
    topo = sorter.sort(BFS)
    print("topoBFS:", topo)

    sample = 30
    RunForwardList = []
    NodeList = []
    for sampleIndex in range(sample):
        RunningVar = {}
        for nodeName in topo:
            node = rp.model.getVertexNode(nodeName)
            #print("nodeName: ",node.vertex)
            #print("tableProb: ",node.tableProb)
            NodeList.append(node.tableProb)
            node.tableProb.getOutput(RunningVar)
        RunForwardList.append(RunningVar)
        
    Observations = { 'I' : 'Cao', 'D' : 'Kho' }
    NodeNameList = topo

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


    for Node in NodeList:
        if Node.NodeName in Observations.keys():
            print(Node.NodeName, Observations[Node.NodeName])
        else:
            print(Node.NodeName)
            indexNumpyRunValue = np.where(NumpyKey==Node.NodeName)[0][0]
            for Value in Node.getValueList():
                print(Value,len(np.where(NumpyRunValue[:,indexNumpyRunValue] == Value)[0])/NumpyRunValue.shape[0])
        print('============================')

if __name__ == "__main__":
    main(sys.argv[1:])    