import sys, getopt, copy
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
    # print("<<<<<Original model>>>>>")
    # rp.model.println()

    tp = ReadTestCase(testfile)
    ques, condit = tp.generate()
    # print("question: ",ques)
    # print("condition: ",condit)
    
    str_out = ""
    for index in range(len(condit)):
        graphModel = copy.deepcopy(rp.model)
        subCond = condit[index][0]
        if len(subCond) > 0:
            # print("===exact inference with condition===")
            str_out += "===exact inference with condition===\n"
            # print("ques[index]:",ques[index]) 
            # print("condit[index]:",condit[index])    
            str_out += "Question: " + str(ques[index]) + "\n"
            str_out += "Condition: " + str(condit[index]) + "\n"
            finalFactor,id_max = ft.condProductVE(graphModel, ques[index], condit[index])
            # print("Probability Table:\n ",finalFactor.tableProb)
            # print("result: ", finalFactor.tableProb[id_max][0])
            str_out += "Probability Table:\n" + str(finalFactor.tableProb) + "\n"
            str_out += "Result: " + str(finalFactor.tableProb[id_max][0]) + "\n"
            str_out += "===== Done Question " + str(index + 1) + " =====" + "\n" + "\n"
        else:
            # print("===exact inference with no condition===")  
            str_out += "===exact inference with no condition===" + "\n"
            # print("ques[index]:",ques[index])
            str_out += "Question: " + str(ques[index]) + "\n"
            finalFactor = ft.sumProductVE(graphModel, ques[index])
            # print("Probability Table:\n ",finalFactor.tableProb)
            str_out += "Probability Table:\n" + str(finalFactor.tableProb) + "\n"
            str_out += "===== Done Question " + str(index + 1) + " =====" + "\n" + "\n"

    file_output = open("output.txt","w")
    file_output.write(str_out) 
    file_output.close()
    print("Done output!")

    # condition = "D=De"
    # ft.reduceElementbyCondition(rp.model, condition)
    # # condition = "I=Cao"
    # # ft.reduceElementbyCondition(rp.model, condition)
    # print("<<<<<Sub model>>>>>")
    # rp.model.println()

    # DFS = 0
    # BFS = 1
    # sorter = TopoSorter(rp.model)
    # topo = sorter.sort(BFS)

    # var2remove = ft.findVartoRemove(topo, ques, condit)
    # print("var2remove: ",var2remove)

    # for condition in condit[0]:
    #     print("condition: ",condition)
    #     ft.reduceElementbyCondition(rp.model, condition)
    
    # listfactor = []
    # for nodeName in topo:
    #     node = rp.model.getVertexNode(nodeName).tableProb
    #     nodeFactor = Factor(node.initTable, node.OrderProb)
    #     listfactor.append(nodeFactor)
    
    # factor = ft.SumProduct(listfactor,var2remove)
    # nodeQuestion = 'G'
    # listfactor = []
    # var2remove = ft.findPath(rp.model, nodeQuestion)
    # for nodeName in var2remove:
    #     print("nodeName: ", nodeName)
    #     node = rp.model.getVertexNode(nodeName).tableProb
    #     nodeFactor = Factor(node.initTable,node.OrderProb)
    #     listfactor.append(nodeFactor)
    # node = rp.model.getVertexNode(nodeQuestion).tableProb
    # nodeFactor = Factor(node.initTable,node.OrderProb)
    # listfactor.append(nodeFactor)

    # # ft.findPath(rp.model, "V4")
    # nodeD = rp.model.getVertexNode("D").tableProb
    # factorD = Factor(nodeD.initTable,nodeD.OrderProb)
    #
    # nodeI = rp.model.getVertexNode("I").tableProb
    # factorI = Factor(nodeI.initTable,nodeI.OrderProb)
    #
    # nodeS = rp.model.getVertexNode("S").tableProb
    # factorS = Factor(nodeS.initTable,nodeS.OrderProb)
    #
    # nodeG = rp.model.getVertexNode("G").tableProb
    # factorG = Factor(nodeG.initTable,nodeG.OrderProb)
    #
    # nodeL = rp.model.getVertexNode("L").tableProb
    # factorL = Factor(nodeL.initTable,nodeL.OrderProb)
    #
    # listfactor = []
    # listfactor.append(factorI)
    # listfactor.append(factorD)
    # listfactor.append(factorS)
    # listfactor.append(factorG)
    # listfactor.append(factorL)


    # DFS = 0
    # BFS = 1
    # sorter = TopoSorter(rp.model)
    # topo = sorter.sort(BFS)

    # remainList = ft.remainNode(var2remove,topo,nodeQuestion)
    # print("nodeQuestion: ",nodeQuestion)
    # print("var2remove: ",var2remove)
    # print("remainList: ",remainList)

    # factorID = ft.SumProduct(listfactor,var2remove)
    # for factor in factorID:
    #     print("order: ", factor.orderProb)
    #     print("value:\n",factor.tableProb)

    # print("************************************************************************")
    # ftft = ft.multiplyAllVertex(factorID)
    # print("order: ", ftft.orderProb)
    # print("value:\n",ftft.tableProb)
    
    # print("+++++++++")
    # result = ft.sum_out(ftft,'L')
    # print("order: ", result.orderProb)
    # print("value:\n",result.tableProb)

    # print("+++++++++")
    # result = ft.sum_out(result,'D')
    # print("order: ", result.orderProb)
    # print("value:\n",result.tableProb)
    # # for factor in listfactor:
    # #     print("order: ", factor.orderProb)
    # #     print("value:\n",factor.tableProb)
    # print("FINALIZE")
    # ft.finalizeProbability(result)

if __name__ == "__main__":
    main(sys.argv[1:])    