#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
    @   String level   : Info/Error
    @   String msg     : The message you want to show
"""


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


def caseParsing(data):
    '''
        step1:解析data中的model，判断其所属的应用任务，比如dsm
        step2：根据dsm解析数据，因为不同的任务解析模板是不一样的，例如dsm需要studyArea，up，down，property。从转换的字典里找
        step3：将解析的数据输入数字土壤制图的推理方法（先案例化+确定案例库名称 ——> 输入通用的相似度计算 ——>结果）

    :return: 结果格式预计还是json返回前端，python中先用字典，不同的任务可能不同，需考虑兼容性
    '''

    return null
