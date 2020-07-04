import sys, getopt
from ReadInput import *
from FactorUtilities import *

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
    ft = FactorUtilities()

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
    print("len a: ",len(a))
    print("a: ",a)
    print("len b: ",len(b))
    print("b: ",b)

    DFS = 0
    BFS = 1
    sorter = TopoSorter(rp.model)
    topo = sorter.sort(BFS)
    print("topoBFS:", topo)

    nodeD = rp.model.getVertexNode("D").tableProb
    nodeG = rp.model.getVertexNode("G").tableProb

    # print("nodeD table", nodeD.initTable)
    # print("nodeD prob", nodeD.OrderProb)

    # print("nodeG table", nodeG.initTable)
    # print("nodeG prob", nodeG.OrderProb)

    result,order_result = ft.multiply(nodeD.initTable,nodeD.OrderProb,nodeG.initTable,nodeG.OrderProb)
    print("order_result: ",order_result)
    print("result: ",result)

    result_sum,order_result_sum = ft.sum_out(result, order_result, "D")
    print("order_result_sum: ",order_result_sum)
    print("result_sum: ",result_sum)



if __name__ == "__main__":
    main(sys.argv[1:])    