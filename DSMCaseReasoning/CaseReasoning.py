import numpy as np
import xlwt as xw
import math
import pandas as pd
from DSMCaseReasoning import NewCase as nc
import Reasoning as rs
import sys
from os import path
# @author Liang-Peng & Wang-Yijie

cur_dir = path.dirname(path.abspath(__file__))

def DSMCaseReasoning(area, arg):
    up = arg['up']
    down = arg['down']
    property = arg['property']
    DEMfile = cur_dir+"\\src\\dem_xc.tif"
    case = nc.NewCase(up, down, property, DEMfile, area)
    newCases = []
    newCases.append(case)
    return rs.generateSimilarity(newCases, cur_dir+"\\src\\cases.xlsx", cur_dir+"\\src\\envClass.xlsx")


if __name__ == '__main__':
    print('input parameters: top layer(cm), bottom layer(cm), target soil property, DEM file')
    up = 0
    down = 10
    property = 15
    DEMfile = sys.path+"src\\dem_xc.tif"

    #initialization type1
    case1 = nc.NewCase(0,50,15)
    case1.set_area(117596)
    case1.set_elevationD(1058)
    case1.set_meanS(6)
    case1.set_SDH(163)
    case1.set_resolution(30)

    # initialization type2
    case = nc.NewCase(up, down, property, DEMfile)














