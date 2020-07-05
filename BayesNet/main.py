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
    # tp = ReadTestCase(testfile)
    # a,b = tp.generate()
    # print("len a: ",len(a))
    # print("a: ",a)
    # print("len b: ",len(b))
    # print("b: ",b)

    # DFS = 0
    # BFS = 1
    # sorter = TopoSorter(rp.model)
    # topo = sorter.sort(BFS)
    # print("topoBFS:", topo)

    nodeD = rp.model.getVertexNode("D").tableProb
    nodeI = rp.model.getVertexNode("I").tableProb
    nodeS = rp.model.getVertexNode("S").tableProb
    nodeG = rp.model.getVertexNode("G").tableProb
    nodeL = rp.model.getVertexNode("L").tableProb

    # print("nodeD table", nodeD.initTable)
    # print("nodeD prob", nodeD.OrderProb)

    # print("nodeG table", nodeG.initTable)
    # print("nodeG prob", nodeG.OrderProb)

    result_mul_D_G,order_result_mul_D_G = ft.multiply(nodeD.initTable,nodeD.OrderProb,nodeG.initTable,nodeG.OrderProb)
    print("order_result_mul_D_G: ",order_result_mul_D_G)
    # print("result_mul_D_G: ",result_mul_D_G)
    ft.println(result_mul_D_G)

    result_sum_out_D,order_result_sum_out_D = ft.sum_out(result_mul_D_G, order_result_mul_D_G, "D")
    print("order_result_sum_out_D: ",order_result_sum_out_D)
    #print("result_sum_out_D: ",result_sum_out_D)
    ft.println(result_sum_out_D)

    result_mul_S_DG, order_result_mul_S_DG = ft.multiply(nodeS.initTable,nodeS.OrderProb,result_sum_out_D,order_result_sum_out_D)
    print("order_result_mul_S_DG: ",order_result_mul_S_DG)
    # print("result_mul_S_DG: ",result_mul_S_DG)
    ft.println(result_mul_S_DG)
    

    result_mul_SDG_I, order_result_mul_SDG_I = ft.multiply(result_mul_S_DG,order_result_mul_S_DG,nodeI.initTable,nodeI.OrderProb)
    print("order_result_mul_SDG_I: ",order_result_mul_SDG_I)
    # print("result_mul_SDG_I: ",result_mul_SDG_I)
    ft.println(result_mul_SDG_I)

    result_sum_out_I,order_result_sum_out_I = ft.sum_out(result_mul_SDG_I, order_result_mul_SDG_I, "I")
    print("order_result_sum_out_I: ",order_result_sum_out_I)
    # print("result_sum_out_I: ",result_sum_out_I)
    ft.println(result_sum_out_I)

    result_sum_out_S,order_result_sum_out_S = ft.sum_out(result_sum_out_I, order_result_sum_out_I, "S")
    print("order_result_sum_out_S: ",order_result_sum_out_S)
    # print("result_sum_out_S: ",result_sum_out_S)
    ft.println(result_sum_out_S)

    result_mul_SDGI_L, order_result_mul_SDGI_L = ft.multiply(result_sum_out_S,order_result_sum_out_S,nodeL.initTable,nodeL.OrderProb)
    print("order_result_mul_SDGI_L: ",order_result_mul_SDGI_L)
    # print("result_mul_SDGI_L: ",result_mul_SDGI_L)
    ft.println(result_mul_SDGI_L)

    result_sum_out_G,order_result_sum_out_G = ft.sum_out(result_mul_SDGI_L, order_result_mul_SDGI_L, "G")
    print("order_result_sum_out_G: ",order_result_sum_out_G)
    # print("result_sum_out_G: ",result_sum_out_G)
    ft.println(result_sum_out_G)

if __name__ == "__main__":
    main(sys.argv[1:])    