import numpy as np
import xlwt as xw
import math
import pandas as pd
# @author Liang-Peng & Wang-Yijie
from enum import Enum
from os import path

class Type(Enum):
    DISCRETE = 'discrete'
    LINEAR = 'linear'
    BELL = 'bell'

def calSimilarity(x_test, x_case, type, params=None):
    #print(Type.DISCRETE, type, params)
    if type == 'discrete':
        return calDiscrete(x_test, x_case)
    elif type == 'linear':
        return calLinear(x_test, x_case, params)
    elif type == 'bell':
        return calBell(x_test, x_case, params)




def findUsedTerrainEnvs(envNames, envClasses,casesEnvs,caseIds):
        envNames_terrain = []
        for index, envClass in enumerate(envClasses):
            if envClass == "R":
                for j in range(0, len(caseIds)):
                    if envNames[index] in casesEnvs[j]:
                        envNames_terrain.append(envNames[index])
                        break

        return envNames_terrain


def y_result(envNames, envClasses, x_ids, casesEnvs, caseIds):
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

def calArea(x_test, x_case):
        similartiys = []
        for i in range(0, len(x_case)):
            similartiy = 2**(-(abs(math.log10(x_test) - math.log10(x_case[i]))/1.5)**0.5)
            similartiys.append(similartiy)
        return similartiys


def calResolution(x_test, x_case):
        similartiys = []
        for i in range(0, len(x_case)):
            if x_test != 0 and x_case[i] != 0:
                similartiy = 2 ** (-(2 * abs(math.log10(x_test) - math.log10(x_case[i]))) ** 0.5)
            elif x_test == 0 and x_case[i] != 0:
                similartiy = 2 ** (-(2 * abs(x_test - math.log10(x_case[i]))) ** 0.5)
            elif x_test != 0 and x_case[i] == 0:
                similartiy = 2 ** (-(2 * abs(math.log10(x_test) - 0)) ** 0.5)
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

def calRelief(x_test, x_case):
        similartiys = []
        for i in range(0, len(x_case)):
            s = abs(x_test - x_case[i])
            similartiy = 1 - s/max(8848 - x_test, x_test)
            similartiys.append(similartiy)
        return similartiys


def calDepth(x_test, x_case):
        similartiys = []
        for i in range(0, len(x_case)):
            s = abs(x_test - x_case[i])
            similartiy = 1 - s/max(200 - x_test, x_test)
            similartiys.append(similartiy)
        return similartiys


def calSlope(x_test, x_case):
        similartiys = []
        for i in range(0, len(x_case)):
            s = abs(x_test - x_case[i])
            similartiy = 1 - s/max(20 - x_test, x_test)
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
    formtable = pd.read_excel(caseData, sheet_name="formalization")
    cases = table.values[:, 2:]

    colNames = formtable.columns.values[1:]
    types = formtable.values[0,1:]
    params = formtable.values[1,1:]
    caseIndicesIds = table.values[:,0]

    distances = np.zeros((len(cases), 2))
    indices = np.zeros((len(cases), 2))
    for j in range(0, len(newCases)):
        similaritys = np.zeros(np.shape(cases))
        newCase = newCases[j]

        for m, colName in enumerate(colNames):
            temp = calSimilarity(newCase.get_parameter(colName), cases[:, m], types[m], params[m])
            similaritys[:, m] = temp
        caseSimilarity = np.min(similaritys, axis=1)
        caseSimilaritySort = np.sort(-caseSimilarity)
        caseSimilaritySortId = np.argsort(-caseSimilarity)
        distances[j,:] = caseSimilaritySort[0:2:1]
        indices[j, :] = caseSimilaritySortId[0:2:1]
    casesTable = pd.read_excel(caseData, sheet_name="Envs")
    caseEnvs = casesTable.values[:, 1:]
    caseIds = casesTable.values[:, 0]

    envsTable = pd.read_excel(envData, sheet_name="class")
    envNames = envsTable.values[:, 0]
    envClassNames = envsTable.values[:,1]
    y, envNames_terrain = y_result(envNames, envClassNames, caseIndicesIds, caseEnvs, caseIds)
    caseSize, envSize = np.shape(y)


    for i in range(0, len(newCases)):
        caseIndex = int(indices[i][1])
        print('case', int(i+1))
        print('most similiar case:', int(y[caseIndex][0]))
        print('similarity:', -distances[i][1])
        print('environmental covariates', end=':')
        result = []
        for j in range(0, envSize):
            if j and y[caseIndex][j] == 1:
                print(envNames_terrain[j-1],end=',')
                result.append(envNames_terrain[j-1])
        print('')
    dic={}
    dic['covariates'] = result
    return dic