
from DSMCaseReasoning import NewCase as nc
import Reasoning as rs
from os import path
# @author Liang-Peng & Wang-Yijie

cur_dir = path.dirname(path.abspath(__file__))

def DSMCaseReasoning(area, arg):
    up = int(arg['up'])
    down = int(arg['down'])
    property = int(arg['property'])
    DEMfile = cur_dir+"\\src\\dem_xc.tif"
    case = nc.NewCase(up, down, property, DEMfile, area)
    newCases = []
    newCases.append(case)
    return rs.generateSimilarity(newCases, cur_dir+"\\src\\cases.xlsx", cur_dir+"\\src\\envClass.xlsx")

'''
if __name__ == '__main__':

    print('input parameters: top layer(cm), bottom layer(cm), target soil property, DEM file')
    up = 0
    down = 50
    property = 15
    DEMfile = cur_dir+"\\src\\dem_xc.tif"

    #initialization type1
    case1 = nc.NewCase(0,100,15)
    case1.set_area(117599)
    case1.set_elevationD(1044)
    case1.set_meanS(6)
    case1.set_SDH(163)
    case1.set_resolution(30)

    # initialization type2
    case = nc.NewCase(up, down, property, DEMfile)
    print('top:', case.get_up())
    print('bottom:', case.get_down())

    print('resolution:', case.get_resolution())
    print('area:', case.get_area())
    print('meanS:', case.get_meanS())
    print('elevation difference:', case.get_elevationD())
    print('SDH:', case.get_SDH())
    newCases = []
    newCases.append(case)
    newCases.append(case1)
    rs.generateSimilarity(newCases, cur_dir + "\\src\\cases.xlsx", cur_dir + "\\src\\envClass.xlsx")
'''












