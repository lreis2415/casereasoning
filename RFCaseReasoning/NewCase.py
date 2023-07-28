from os import path
from osgeo import gdal
import numpy as np
from CaseFormat import Case
cur_dir = path.dirname(path.abspath(__file__))

class NewCase(Case):
    def __init__(self, typenum=None, studyarea = [0, 0, 100, 100]):
        '''
        研究区范围：studyarea
        :案例形式化因子： typenum类别数
        :案例形式化因子： resolution分辨率
        '''
        # 案例形式化因子
        self.set_parameter('typenum', typenum)
        #self.__typenum = typenum
        self.__resolution = self.calculate_parameter('resolution')
        # 研究区范围变量
        self.__left = studyarea[0]
        self.__right = studyarea[1]
        self.__top = studyarea[2]
        self.__bottom = studyarea[3]
    #案例形式化因子计算
    def calculate_resolution(self):
        resolution = None
        return resolution





