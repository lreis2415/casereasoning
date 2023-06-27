import numpy as np
import xlwt as xw
import math
import pandas as pd
# @author Liang-Peng & Wang-Yijie


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


def generateSimilarity(newCasesExcelPath):
    excelPath = "D:\\DSM_selection_optimization\\test0416\\cases.xlsx"
    reslutionSimLog = ["resolution", "SDH"]
    depthSimLog = ["up", "down"]
    table = pd.read_excel(excelPath, sheet_name="cases")
    newCasesTable = pd.read_excel(newCasesExcelPath, sheet_name="cases")
    cases = table.values[:, 2:]
    newCases = newCasesTable.values[:, 2:]
    depthLogIndex = []
    reslutionLogIndex = []
    colNames = table.columns.values[2:]
    caseIndicesIds = table.values[:,0]
    for index, colName in enumerate(colNames):
        if colName == 'property':
            propertyIndex = index
        if colName == 'elevation difference':
            edIndex = index
        if colName == 'meanS':
            msIndex = index
        if colName in depthSimLog:
            depthLogIndex.append(index)
        if colName == 'area':
            areaIndex = index
        if colName in reslutionSimLog:
            reslutionLogIndex.append(index)
    distances = np.zeros((len(cases), 2))
    indices = np.zeros((len(cases), 2))
    for j in range(0, len(newCases)):
        similaritys = np.zeros(np.shape(cases))
        newCase = newCases[j]
        for m in range(0, len(cases[j])):
            temp = []
            # if (m == propertyIndex) or (m == classification):
            if m == propertyIndex:
                temp = calDiscrete(newCase[m], cases[:, m])
            elif m == edIndex:
                temp = calRelief(newCase[m], cases[:, m])
            elif m == areaIndex:
                temp = calArea(newCase[m], cases[:, m])
            elif m == msIndex:
                temp = calSlope(newCase[m], cases[:, m])
            elif m in reslutionLogIndex:
                 temp = calResolution(newCase[m], cases[:, m])
            elif m in depthLogIndex:
                temp = calDepth(newCase[m], cases[:, m])
            similaritys[:, m] = temp
        caseSimilarity = np.min(similaritys, axis=1)
        caseSimilaritySort = np.sort(-caseSimilarity)
        caseSimilaritySortId = np.argsort(-caseSimilarity)
        distances[j,:] = caseSimilaritySort[0:2:1]
        indices[j, :] = caseSimilaritySortId[0:2:1]
    casesTable = pd.read_excel(excelPath, sheet_name="Envs")
    caseEnvs = casesTable.values[:, 1:]
    caseIds = casesTable.values[:, 0]
    envsTable = pd.read_excel("D:\\DSM_selection_optimization\\test0416\\envClass.xlsx", sheet_name="class")
    envNames = envsTable.values[:, 0]
    envClassNames = envsTable.values[:,1]
    y, envNames_terrain = y_result(envNames, envClassNames, caseIndicesIds, caseEnvs, caseIds)
    caseSize, envSize = np.shape(y)
    wb = xw.Workbook()
    ws_predict_env = wb.add_sheet('predict_env')
    ws_predict_env_score = wb.add_sheet('predict_env_score')
    for k in range(0, len(envNames_terrain)):
        ws_predict_env.write(0, k + 1, envNames_terrain[k])
    for i in range(0, len(newCases)):
        caseIndex = int(indices[i][1])
        for j in range(0, envSize):
            ws_predict_env.write(i + 1, j, y[caseIndex][j])
        ws_predict_env_score.write(i + 1, 1, -distances[i][1])
    wb.save('D:\\DSM_selection_optimization\\test0416\\finalStatistic_MS.xls')


if __name__ == '__main__':
    newCasesExcelPath = "D:\\DSM_selection_optimization\\test0416\\newCase.xlsx"
    generateSimilarity(newCasesExcelPath)






