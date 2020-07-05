import numpy as np
import copy

class FactorUtilities():
    # def __init__(self):
    #     return None

    def multiply(self, factor1, order_factor1, factor2, order_factor2):
        #find all the common variables between the two factors:
        common_vars = []
        f1 = []
        f2 = []

        for char in order_factor1:
            if char in order_factor2:
                common_vars.append(char)
            else:
                f1.append(char)

        for char in order_factor2:
            if char not in order_factor1:
                f2.append(char)

        all_vars = f1+common_vars+f2
        num_vars = len(all_vars)
        # print("f1: ",f1)
        # print("f2: ",f2)
        # print("common_vars: ",common_vars)
        # print("all_vars: ",all_vars)
        #find index common column
        index_common_f1 = order_factor1.index(common_vars[0])

        # print("index_common_f1: ",index_common_f1)
        
        #swap common column in factor1 to at the end
        if f1 != []:
            self.swapCommon(factor1,index_common_f1,False)
            self.swapCommon(order_factor1,index_common_f1,False)
        
        #find index common column
        index_common_f2 = order_factor2.index(common_vars[0])
        # print("index_common_f2: ",index_common_f2)

        #swap common column in factor2 to at the beginning
        if f2 != []:
            self.swapCommon(factor2,index_common_f2,True)
            self.swapCommon(order_factor2,index_common_f2,True)

        #prepare list input
        listInput = []

        #search through factor 1
        for var in order_factor1:
            # print("var1: ",var)
            tmp = self.uniqueElement([factor1[i][order_factor1.index(var[0])] for i in range(len(factor1))])
            listInput.append(tmp)

        #search through factor 2, skip common at the beginning of factor 2
        sub_order_factor2 = order_factor2[1:]
        # print("sub_order_factor2: ",sub_order_factor2)
        for var in sub_order_factor2:
            # print("var2: ",var)
            tmp = self.uniqueElement([factor2[i][order_factor2.index(var[0])] for i in range(len(factor2))])
            listInput.append(tmp)

        # print("listInput: ",listInput)
        #generate probability combinations
        result = self.parsing_combinationProb(listInput)
        # print("result: ",result)

        #add value of probability combinations
        for row in range(len(result)):
            key1 = result[row][:len(order_factor1)]
            key2 = result[row][len(order_factor1) - len(common_vars):]
            # print("key1: ",key1)
            # print("key2: ",key2)
            value1 = self.get_value(factor1,tuple(key1))
            value2 = self.get_value(factor2,tuple(key2))
            # print("value1: ",value1)
            # print("value2: ",value2)
            product = value1 * value2
            result[row].append(product)
        
        return result,all_vars

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

    def get_value(self, factor, key):
        newd = dict()
        for i in range(len(factor)):
            newd.update({tuple([factor[i][j] for j in range(len(factor[i])-1)]):factor[i][-1]})
        return newd.get(key)

    def swapCommon(self, factor, key, begin):
        if type(factor[0][-1]) is float:
            if begin: #swap common to the first row
                for row in range(len(factor)):
                    tmp = factor[row][0]
                    factor[row][0] = factor[row][key]
                    factor[row][key] = tmp
            else: # swap common to the latest row
                for row in range(len(factor)):
                    tmp = factor[row][-2]
                    factor[row][-2] = factor[row][key]
                    factor[row][key] = tmp
        else:
            if begin: #swap common to the first row
                tmp = factor[0]
                factor[0] = factor[key]
                factor[key] = tmp
            else: # swap common to the latest row
                tmp = factor[-1]
                factor[-1] = factor[key]
                factor[key] = tmp

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

    def sum_out(self, factor, order_factor, key):
        #remove column key and value
        new_factor = copy.deepcopy(factor)
        self.removeColumn(new_factor, order_factor, key)
        self.removeValue(new_factor)

        #sum_out
        newProbList = [] #list for probability combinations
        newValueList = [] #list for sum_out value
        count_index = 0
        for row in range(len(new_factor)):
            entry = new_factor[row]
            # print("entry:",entry)
            # print("value:",factor[row][-1])
            if entry not in newProbList:
                newProbList.append(entry)
                newValueList.append(factor[row][-1])
                count_index += 1
            else:
                index = newProbList.index(entry)
                # print("index", index)
                # print("newValueList[index]: ",newValueList[index])
                # print("factor[row][-1]: ",factor[row][-1])
                # print("cong don: ",newValueList[index] + factor[row][-1])
                newValueList[index] = newValueList[index] + factor[row][-1]

        #merge list of probability combinations and list of value
        for row in range(len(newProbList)):
            newProbList[row].append(newValueList[row])
        return newProbList,order_factor

    ##function uilities for sum_out
    def removeColumn(self, factor, order_factor, variable):
        index_column = order_factor.index(variable)
        order_factor.pop(index_column)
        for row in range(len(factor)):
            factor[row].pop(index_column)

    def removeValue(self, factor):
        for row in range(len(factor)):
            factor[row].pop(-1)
