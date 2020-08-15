import numpy as np
import copy
from DGraphModel import *

class Factor():
    def __init__(self, initTableProb, initOrderProb):
        self.tableProb = initTableProb
        self.orderProb = initOrderProb

    def updateFactorElement(self, newTableProb= None, newOrderProb= None):
        if newTableProb is not None:
            self.tableProb = newTableProb

        if newOrderProb is not None:    
            self.orderProb = newOrderProb

    def updateFactor(self, newFactor):
        self.updateFactorElement(newFactor.tableProb, newFactor.orderProb)

class FactorUtilities(Factor):
    def __init__(self):
        self.DFS = 0
        self.BFS = 1

    def multiply(self, factor1, factor2):
        print("======enter multiply=======")
        print("factor 1 origin: ",factor1.orderProb)
        print("factor 1 origin: ",factor1.tableProb)
        print("factor 2 origin: ",factor2.orderProb)
        print("factor 2 origin: ",factor2.tableProb)
        #find all the common variables between the two factors:
        common_vars = []
        f1 = []
        f2 = []

        for char in factor1.orderProb:
            if char in factor2.orderProb:
                common_vars.append(char)
            else:
                f1.append(char)

        for char in factor2.orderProb:
            if char not in factor1.orderProb:
                f2.append(char)

        all_vars = f1+common_vars+f2
        num_vars = len(all_vars)
        print("f1: ",f1)
        print("f2: ",f2)
        print("common_vars: ",common_vars)
        print("all_vars: ",all_vars)
        #find index common column
        index_common_f1 = factor1.orderProb.index(common_vars[0])

        print("index_common_f1: ",index_common_f1)
        print("factor 1 before: ",factor1.orderProb)
        print("factor 1 before: ",factor1.tableProb)
        #swap common column in factor1 to at the end
        if f1 != []:
            self.swapCommon(factor1.tableProb,index_common_f1,False)
            self.swapCommon(factor1.orderProb,index_common_f1,False)
        
        print("factor 1 after: ",factor1.orderProb)
        print("factor 1 after: ",factor1.tableProb)

        print("factor 2 before: ",factor2.orderProb)
        print("factor 2 before: ",factor2.tableProb)
        #find index common column
        index_common_f2 = factor2.orderProb.index(common_vars[0])
        print("index_common_f2: ",index_common_f2)

        #swap common column in factor2 to at the beginning
        if f2 != []:
            self.swapCommon(factor2.tableProb,index_common_f2,True)
            self.swapCommon(factor2.orderProb,index_common_f2,True)

        print("factor 2 after: ",factor2.orderProb)
        print("factor 2 after: ",factor2.tableProb)
        #prepare list input
        listInput = []

        #search through factor 1
        for var in factor1.orderProb:
            print("var1: ",var)
            tmp = self.uniqueElement([factor1.tableProb[i][factor1.orderProb.index(var[0])] for i in range(len(factor1.tableProb))])
            listInput.append(tmp)

        #search through factor 2, skip common at the beginning of factor 2
        sub_order_factor2 = factor2.orderProb[1:]
        print("sub_order_factor2: ",sub_order_factor2)
        for var in sub_order_factor2:
            print("var2: ",var)
            tmp = self.uniqueElement([factor2.tableProb[i][factor2.orderProb.index(var[0])] for i in range(len(factor2.tableProb))])
            listInput.append(tmp)

        print("listInput: ",listInput)
        #generate probability combinations
        result = self.parsing_combinationProb(listInput)
        print("result: ",result)

        #add value of probability combinations
        for row in range(len(result)):
            print("--------")
            print("factor1: ",factor1.orderProb)
            print("factor2: ",factor2.orderProb)
            key1 = result[row][:len(factor1.orderProb)]
            key2 = result[row][len(factor1.orderProb) - len(common_vars):]
            print("key1: ",key1)
            print("key2: ",key2)
            value1 = self.get_value(factor1.tableProb,tuple(key1))
            value2 = self.get_value(factor2.tableProb,tuple(key2))
            print("value1: ",value1)
            print("value2: ",value2)
            product = value1 * value2
            result[row].append(product)
        
        print("======Exit multiply==========")
        self.reOrderAllVars(factor1.orderProb, factor2.orderProb, all_vars)
        return Factor(result, all_vars)

    ##function uilities for multiply
    def uniqueElement(self, observation):
        # intilize a null list
        unique_list = []
        # traverse for all elements
        for x in observation:
            # check if exists in unique_list or not
            if x not in unique_list:
                unique_list.append(x)
        return unique_list

    def get_value(self, factorTableProb, key):
        newd = dict()
        for i in range(len(factorTableProb)):
            newd.update({tuple([factorTableProb[i][j] for j in range(len(factorTableProb[i])-1)]):factorTableProb[i][-1]})
        return newd.get(key)

    def swapCommon(self, factorTableProb, key, begin):
        if type(factorTableProb[0][-1]) is float:
            if begin: #swap common to the first row
                for row in range(len(factorTableProb)):
                    tmp = factorTableProb[row][0]
                    factorTableProb[row][0] = factorTableProb[row][key]
                    factorTableProb[row][key] = tmp
            else: # swap common to the latest row
                for row in range(len(factorTableProb)):
                    tmp = factorTableProb[row][-2]
                    factorTableProb[row][-2] = factorTableProb[row][key]
                    factorTableProb[row][key] = tmp
        else:
            if begin: #swap common to the first row
                tmp = factorTableProb[0]
                factorTableProb[0] = factorTableProb[key]
                factorTableProb[key] = tmp
            else: # swap common to the latest row
                tmp = factorTableProb[-1]
                factorTableProb[-1] = factorTableProb[key]
                factorTableProb[key] = tmp

    def parsing_combinationProb(self, listProb):
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
                output.append(aResult)
                count += 1
            #print(output)
            return output

    def reOrderAllVars(self, orderFactor1, orderFactor2, all_vars):
        print('all_vars before: ', all_vars)
        print('orderFactor1: ',orderFactor1)
        print('orderFactor2: ',orderFactor2)
        index_all_vars = 0
        for index in range(len(all_vars)):
            # print("index:", index)
            if index < len(orderFactor1) - 1:
                char = orderFactor1[index]
                # print("char orderFactor1:",char)
            else:
                char = orderFactor2[index + 1 - len(orderFactor1)]
                # print("char orderFactor2:",char)
            if char in all_vars:
                tmp_index = all_vars.index(char)
                # print("tmp_index:",tmp_index)
                tmp_char = all_vars[index_all_vars]
                # print("tmp_char:",tmp_char)
                all_vars[index_all_vars] = all_vars[tmp_index]
                all_vars[tmp_index] = tmp_char
                index_all_vars += 1
        print('all_vars after: ', all_vars)

    def sum_out(self, factor, key):
        #remove column key and value
        new_factor = copy.deepcopy(factor.tableProb)
        self.removeColumn(new_factor, factor.orderProb, key)
        self.removeValue(new_factor)

        #sum_out
        newProbList = [] #list for probability combinations
        newValueList = [] #list for sum_out value
        count_index = 0
        for row in range(len(new_factor)):
            entry = new_factor[row]
            # print("entry:",entry)
            # print("value:",factor.tableProb[row][-1])
            if entry not in newProbList:
                newProbList.append(entry)
                newValueList.append(factor.tableProb[row][-1])
                count_index += 1
            else:
                index = newProbList.index(entry)
                # print("index", index)
                # print("newValueList[index]: ",newValueList[index])
                # print("factor[row][-1]: ",factor.tableProb[row][-1])
                # print("cong don: ",newValueList[index] + factor.tableProb[row][-1])
                newValueList[index] = newValueList[index] + factor.tableProb[row][-1]

        #merge list of probability combinations and list of value
        for row in range(len(newProbList)):
            newProbList[row].append(newValueList[row])
        return Factor(newProbList, factor.orderProb)

    ##function uilities for sum_out
    def removeColumn(self, factor, order_factor, variable):
        index_column = order_factor.index(variable)
        order_factor.pop(index_column)
        for row in range(len(factor)):
            factor[row].pop(index_column)

    def removeValue(self, factor):
        for row in range(len(factor)):
            factor[row].pop(-1)

    def println(self, factor):
        for row in range(len(factor)):
            strr = str(factor[row])
            print(strr)
            
    ##fucntion reduce probability elements by condition
    def _reduceElementbyCondition(self, factor, element, value):
        index_element = factor.orderProb.index(element)
        num_row = len(factor.tableProb)
        row = 0
        while row < num_row:
            if value != factor.tableProb[row][index_element]:
                factor.tableProb.remove(factor.tableProb[row])
                row = 0
                num_row = len(factor.tableProb)
            else:
                row += 1

    def reduceElementbyCondition(self, model, condition):
        sorter = TopoSorter(model)
        topoList = sorter.sort(self.BFS)
        
        element = condition.split('=')[0]
        value = condition.split('=')[1]

        #search vertex has condition
        for vertex in topoList:
            node = model.getVertexNode(vertex).tableProb
            ft = Factor(node.initTable, node.OrderProb)
            if element in node.OrderProb:
                self._reduceElementbyCondition(ft, element, value)

    def SumProduct(self, factorList, var2remove):
        for var in var2remove:
            print("var: ",var)
            #1.1
            factor_contain_var = []
            for factor in factorList:
                print("factor.orderProb: ",factor.orderProb)
                if var in factor.orderProb:
                    print("ting")
                    factor_contain_var.append(factor)
            print("factor_contain_var: ",len(factor_contain_var))
            #1.2
            if len(factor_contain_var) >= 2:
                newfactor = self.multiply(factor_contain_var[0],factor_contain_var[1])
                for index in range(2,len(factor_contain_var)):
                    newfactor = self.multiply(newfactor, factor_contain_var[index])
            elif len(factor_contain_var) == 1:
                newfactor = factor_contain_var[0]

            #1.3
            newfactor = self.sum_out(newfactor, var)

            #1.4 & 1.5
            self.updateFactorList(factorList, factor_contain_var, newfactor)
            print("===========")
            for lst in factorList:
                print("lst: ",lst.orderProb)
                print("lst value: ",lst.tableProb)
            print("===========")
        return factorList
        # self.sumoutRemainNode(remainNode,factorList)

    def updateFactorList(self,factorlist, factor_contain_var, newfactor):
         for factor in factor_contain_var:
             factorlist.remove(factor)
         factorlist.insert(0, newfactor)

    def findPath(self, graph, nodeName):
        list_node_before = []
        list_node_to_find = []
        list_node_to_find.append(nodeName)
        while True:
            list_node_to = []
            # print("list_node_to_find: ", list_node_to_find)
            for node_des in list_node_to_find:
                # print("node_des: ",node_des)
                list_node = graph.getInwardEdges(node_des)
                for i in range(len(list_node)):
                    list_node_to.append(list_node[i])
                    if list_node[i] and list_node[i] not in list_node_before:
                        list_node_before.append(list_node[i])
                # print("list_node: ",list_node)
                # print("list_node_to: ",list_node_to)

            if list_node_to:
                list_node_to_find = list_node_to
            else:
                break
        return self.sortOrderNode(graph,list_node_before)


    def sortOrderNode(self, graph, listNode):
        sorter = TopoSorter(graph)
        topo = sorter.sort(self.BFS)
        # print("listNode: ",listNode)
        # print("topo: ",topo)
        index_listNode = 0
        # print("index_listNode: ",index_listNode)
        for index in range(len(topo)):
            charTopo = topo[index]
            # print("charTopo: ",charTopo)
            if charTopo in listNode:
                tmp_index = listNode.index(charTopo)
                # print("tmp_index: ",tmp_index)
                tmp_char = listNode[index_listNode]
                # print("tmp_char: ",tmp_char)
                # print("listNode[index_listNode]: {} =  listNode[tmp_index]: {}".format(listNode[index_listNode], listNode[tmp_index]))
                listNode[index_listNode] = listNode[tmp_index]
                # print("listNode[tmp_index]: {} =  tmp_char: {}".format(listNode[tmp_index], tmp_char))
                listNode[tmp_index] = tmp_char
                index_listNode += 1
            # print("index_listNode: ",index_listNode)
            # print("listNode: ",listNode)
            # print("============")
        return listNode


    # def remainNode(self, listNode, listTopo, nodeQuesttion):
    #     for i in range(len(listNode)):
    #         listTopo.remove(listNode[i])
    #     listTopo.remove(nodeQuesttion)
    #     return listTopo
    #
    # def sumoutRemainNode(self, remainNodeList, factorList):
    #     for lst in factorList:
    #         print("lst order:", lst.orderProb)
    #         for node in remainNodeList:
    #             print("node: ", node)
    #             if node in lst.orderProb:
    #                 print("ting tong")
    #                 index = lst.orderProb.index(node)
    #                 newfactor = self.sum_out(factorList[index], node)
    #                 factorList.remove(factorList[index])
    #                 factorList.insert(0, newfactor)

    def findVartoRemove(self, topo_original, varQuestion, varCondition):
        topo = topo_original.copy()
        for charQ in varQuestion[0]:
            print("delete: ",charQ)
            topo.remove(charQ)

        for charE in varCondition[0]:
            char = charE.split('=')[0]
            print("delete: ",char)
            topo.remove(char)
        return topo


    def multiplyAllVertex(self, factorList):
        firstFactor = factorList[0]
        secondFactor = factorList[1]
        factorList.remove(firstFactor)
        factorList.remove(secondFactor)
        print("firstFactor: ",firstFactor.orderProb)
        print("secondFactor: ",secondFactor.orderProb)
        tmp_result = self.multiply(firstFactor, secondFactor)

        for factor in factorList:
            print("factor: ",factor.orderProb)
            tmp_result = self.multiply(tmp_result, factor)
        return tmp_result

    def finalizeProbability(self, factor):
        sumProb = 0
        probLists = []
        for element in factor.tableProb:
            sumProb += element[-1]

        for element in factor.tableProb:
            element[-1] = element[-1] / sumProb
            probLists.append(element[-1])

        print("order: ", factor.orderProb)
        print("value:\n",factor.tableProb)
        print("probLists: ",probLists)

        my_array = np.array(probLists)
        id_max  = np.argmax(my_array)

        print("RESULT: ", factor.tableProb[id_max][0])


