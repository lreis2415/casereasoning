#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
    @   String level   : Info/Error
    @   String msg     : The message you want to show
"""
import codecs
import datetime
from os import path

from DSMCaseReasoning import CaseReasoning as DSMcr
from RFCaseReasoning import CaseReasoning as RFcr


def echoMsg(self, level, msg, timestr=datetime.datetime.now().strftime('%Y.%m.%d-%H:%M:%S')):
    logFilePath = path.dirname(path.dirname(__file__)) + '/log.txt'
    f = codecs.open(logFilePath, 'a', 'utf-8')
    if level == 'Info':
        str = '[Info] %s\n[Time] %s' % (msg, timestr)
        self.printInfo(str)
        self.printInfo('-------------------------')
        f.write('[Info] %s\r\n[Time] %s\r\n' % (msg, timestr))
        f.write('-------------------------\r\n')
    elif level == 'Error':
        str = '[Error] %s\n[Time] %s' % (msg, timestr)
        self.printInfo(str)
        self.printInfo('-------------------------')
        f.write('[Error] %s\r\n[Time] %s\r\n' % (msg, timestr))
        f.write('-------------------------\r\n')
    f.close()


def caseParsing(data, null=None):
    """
        step1:解析data
        step2：根据dsm解析数据，因为不同的任务解析模板是不一样的，例如dsm需要studyArea，up，down，property。从转换的字典里找
        step3：将解析的数据输入相应的推理方法，如DSMCaseReasoning，RFCaseReasoning（RF和iPSM的推理方法相同）

    :return: 结果为推荐的环境变量，格式为字典
    """
    # step1：解析数据
    model = data['model']
    arg = data['arg']
    result = null
    # step2:选择model
    if model == 'iPSM':
        studyArea = data['studyArea']
        if studyArea is not None and (studyArea[0] >= studyArea[1] or studyArea[2] <= studyArea[3]):
            return 'invalid input study area'
        # step3：将解析的数据输入相应的推理方法
        scenario, result = DSMcr.DSMCaseReasoning(studyArea, arg)
    elif model == 'RF':
        studyArea = data['studyArea']
        # step3：将解析的数据输入相应的推理方法
        result = RFcr.RFCaseReasoning(studyArea, arg)

    return scenario, result
    # return #结果字典


def caseParsingEGC(data, null=None):
    '''
        step1:解析data
        step2：根据dsm解析数据，因为不同的任务解析模板是不一样的，例如dsm需要studyArea，up，down，property。从转换的字典里找
        step3：将解析的数据输入相应的推理方法，如DSMCaseReasoning，RFCaseReasoning

    :return: 结果为推荐的环境变量，格式为字典
    '''
    # step1：解析数据
    model = data['model']
    arg = data['arg']
    result = null
    # step2:选择model
    if model == 'iPSM':
        studyArea = data['studyArea']
        if studyArea is not None:
            newArea = [studyArea[0], studyArea[0], studyArea[1], studyArea[1]]
            # return 'invalid input study area'
            # step3：将解析的数据输入相应的推理方法
            result = DSMcr.DSMCaseReasoning(newArea, arg)
        else:
            return 'invalid input study area'
    elif model == 'RF':
        studyArea = data['studyArea']
        # step3：将解析的数据输入相应的推理方法
        result = RFcr.RFCaseReasoning(studyArea, arg)

    return result
    # return #结果字典
