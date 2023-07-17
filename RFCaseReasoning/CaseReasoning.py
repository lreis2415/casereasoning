from DSMCaseReasoning import NewCase as nc
import Reasoning as rs
from os import path

cur_dir = path.dirname(path.abspath(__file__))

'''
step1: 提取参数
step2：实例化NewCase类新建一个案例
step3：通过generateSimilarity计算新案例与案例库中案例相似度
'''
def RFCaseReasoning(area, arg):
    #参数提取
    typenum = arg['typenum']
    #新建案例
    case = nc.NewCase(typenum, area)
    newCases = []
    newCases.append(case)
    #案例库
    caseData = cur_dir+"\\src\\cases.xlsx"
    #环境变量库
    envData = cur_dir+"\\src\\envClass.xlsx"

    return rs.generateSimilarity(newCases, caseData, envData)











