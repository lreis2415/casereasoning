import numpy as np
import math
import pandas as pd
# @author Liang-Peng & Wang-Yijie
from enum import Enum
from os import path
'''
class Type(Enum):
    DISCRETE = 'discrete'
    LINEAR = 'linear'
    BELL = 'bell'
'''


def findUsedTerrainEnvs(envNames, envClasses,casesEnvs,caseIds):
        envNames_terrain = []
        for index, envClass in enumerate(envClasses):
            if envClass == "R":
                for j in range(0, len(caseIds)):
                    if envNames[index] in casesEnvs[j]:
                        envNames_terrain.append(envNames[index])
                        break

        return envNames_terrain


def case_Envtable(envNames, envClasses, x_ids, casesEnvs, caseIds):
        envNames_terrain = []
        for index, envClass in enumerate(envClasses):
            if envClass == "R":
                envNames_terrain.append(envNames[index])
        y_index = len(envNames_terrain) + 1  # add a col for record the id of case
        x_index = len(x_ids)
        y = np.zeros([x_index, y_index])
        y[:, 0] = x_ids
        for x_index, x_id in enumerate(x_ids):
            caseEnvs_id = np.argwhere(caseIds == x_id)
            caseEnvs = casesEnvs[caseEnvs_id]
            for y_index, envName in enumerate(envNames_terrain):
                if envName in caseEnvs:
                    y[x_index][y_index + 1] = 1

        return y,envNames_terrain

def calSimilarity(x_test, x_case, type, params=None):
    if type == 'discrete':
        return calDiscrete(x_test, x_case)
    elif type == 'linear':
        return calLinear(x_test, x_case, params)
    elif type == 'bell':
        return calBell(x_test, x_case, params)

def calBell(x_test, x_case, params):
    similartiys = []
    for i in range(0, len(x_case)):
        if x_test != 0 and x_case[i] != 0:
            similartiy = 2 ** (-(params * abs(math.log10(x_test) - math.log10(x_case[i]))) ** 0.5)
        elif x_test == 0 and x_case[i] != 0:
            similartiy = 2 ** (-(params * abs(x_test - math.log10(x_case[i]))) ** 0.5)
        elif x_test != 0 and x_case[i] == 0:
            similartiy = 2 ** (-(params * abs(math.log10(x_test) - 0)) ** 0.5)
        elif x_test == 0 and x_case[i] == 0:
            similartiy = 1
        similartiys.append(similartiy)
    return similartiys


def calLinear(x_test, x_case, valMax):
        similartiys = []
        for i in range(0, len(x_case)):
            s = abs(x_test - x_case[i])
            similartiy = 1 - s/max(valMax - x_test, x_test)
            similartiys.append(similartiy)
        return similartiys


def calDiscrete(x_test, x_case):
        similartiys = []
        for i in range(0, len(x_case)):
            if (x_test - x_case[i]) == 0:
                similartiy = 1
            else:
                similartiy = 0
            similartiys.append(similartiy)
        return similartiys

def generateSimilarity(newCases, caseData = None, envData = None):
    if caseData == None or path.exists(caseData) == 0:
        print('no database found')
        return
    table = pd.read_excel(caseData, sheet_name="cases")
    cases = table.values[:, 2:]
    caseIndicesIds = table.values[:, 0]
    formtable = pd.read_excel(caseData, sheet_name="formalization")
    colNames = formtable.columns.values[1:]
    types = formtable.values[0,1:]
    params = formtable.values[1,1:]
    #计算新案例与案例库各案例相似度
    distances = np.zeros((len(cases), 3))
    indices = np.zeros((len(cases), 3))
    for j in range(0, len(newCases)):
        similaritys = np.zeros(np.shape(cases))
        newCase = newCases[j]

        for m, colName in enumerate(colNames):
            temp = calSimilarity(newCase.get_parameter(colName), cases[:, m], types[m], params[m])
            similaritys[:, m] = temp
        caseSimilarity = np.min(similaritys, axis=1)
        caseSimilaritySort = np.sort(-caseSimilarity)
        caseSimilaritySortId = np.argsort(-caseSimilarity)
        #提取第二相似案例
        distances[j,:] = caseSimilaritySort[0:3:1]
        indices[j, :] = caseSimilaritySortId[0:3:1]

    #查找各案例的环境变量
    casesTable = pd.read_excel(caseData, sheet_name="Envs")
    caseEnvs = casesTable.values[:, 1:]
    caseIds = casesTable.values[:, 0]
    envsTable = pd.read_excel(envData, sheet_name="class")
    envNames = envsTable.values[:, 0]
    envClassNames = envsTable.values[:,1]
    y, envNames_terrain = case_Envtable(envNames, envClassNames, caseIndicesIds, caseEnvs, caseIds)
    caseSize, envSize = np.shape(y)

    dic={}
    #将推荐环境变量存入result
    for i in range(0, len(newCases)):

        recCase = {}
        caseIndex = int(indices[i][0])
        recCase['case id'] = str(int(y[caseIndex][0]))
        result = []
        print('most similiar case:', int(y[caseIndex][0]))
        print('similarity:', -distances[i][0])
        print('environmental covariates', end=':')
        for j in range(0, envSize):
            if j and y[caseIndex][j] == 1:
                print(envNames_terrain[j - 1], end=',')
                result.append(envNames_terrain[j - 1])
        recCase['covariates'] = result
        dic['most similiar case'] = recCase

        newcase = {}
        for m, colName in enumerate(colNames):
            newcase[colName] = format(newCases[0].get_parameter(colName), '.0f')
        dic['case formalization']=newcase

        simicase = {}
        for k in range(0,3):
            caseIndex = int(indices[i][k])
            cov = []
            cases = {}
            if -distances[i][k] > 0:
                key = 'similiar case '+str(k+1)#+ str(int(y[caseIndex][0]))
                #print('most similiar case:', int(y[caseIndex][0]))
                #print('similarity:', -distances[i][k])
                #print('environmental covariates', end=':')
                result = []
                for j in range(0, envSize):
                    if j and y[caseIndex][j] == 1:
                        #print(envNames_terrain[j-1],end=',')
                        result.append(envNames_terrain[j-1])
                cases['case id'] = str(int(y[caseIndex][0]))
                cases['covariates'] = result
                cases['similarity'] = format(-distances[i][k], '.3f')
                simicase[key] = cases
                #print('')
        dic['similiar cases']=simicase
    #print(dic)
    #max_similarity = max(float(case["similarity"]) for case in dic.values())
    #result = [case["covariates"] for case in dic.values() if float(case["similarity"]) == max_similarity]
    #print(result[0])
    return dic