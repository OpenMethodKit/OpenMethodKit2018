import pandas as pd
import numpy as np
from statistics import *
pd.options.mode.chained_assignment = None  # default='warn'
import seaborn as sns
sns.set(style="white") #设置绘图背景
pd.set_option('precision', 2)
import pandas as pd
from numpy import *
import os
from scipy import stats
from pandas import Series,DataFrame
from decimal import *


def deleteZero(Interval):
    Interval = np.array(Interval)
    ResultI = []
    for i in range(len(Interval)):
        if(Interval[i] !=0 ):
            ResultI.append(Interval[i])
    return ResultI

def GlobalStatistic(Interval):


    # mode
    # print("Sign",Interval)
    df = DataFrame()
    df['Interval'] = Interval
    modeI = mode(df['Interval'])
    Interval = np.array(Interval)

    lenI = len(Interval)
    # max min
    maxInterval = max(Interval)
    minInterval = min(Interval)
    # print(minInterval,maxInterval,minPrice,maxPrice)

    meanI = Interval.sum() / (lenI - 1)
    # print(meanI,meanP)

    # zscore

    # std
    stdI = Interval.std()
    # print(stdI,stdP)

    CVI = stdI / meanI
    # print(CVI,CVP)

    skewI = np.sum(np.power((Interval - meanI), 3)) / (lenI * np.power(stdI, 3))

    kurtI = np.sum(np.power(Interval - meanI, 4)) / (lenI * np.power(stdI, 4)) - 3
    # print(np.sum(np.power(Interval - meanI, 4)), "and", (lenI * np.power(stdI, 4)) - 3)
    result = [minInterval, maxInterval, meanI, modeI, stdI, CVI, skewI, kurtI]
    result = [("%.2f" % i) for i in result]
    # print(result)
    return result
# 定义文件夹
datapath = '/Users/lixuefei/Desktop/Class'

# 抽取数据所在的文件列表
filelist = os.listdir(datapath)
# 定义列表名称
dataname = ['Type', 'OS', 'Region', 'Time', 'Price', 'Interval']

fo = open("fooInterval.csv", "w")
fo.write("name,minInterval,maxInterval,meanI,modeI,stdI,CVI,skewI,kurtI\n")

for files in filelist:
    file_name = os.path.splitext(files)  # 获取切片好的文件名
    if file_name[1] == '.txt':
        # 数据文件的地址
        cpath = os.path.join(datapath, files)
        service_name = file_name[0]
        df = pd.read_table(cpath,names=dataname)
        df = df.drop(['Type', 'OS', 'Region'],axis = 1)
        df['Time'] = pd.to_datetime(df['Time'])
        df = df.set_index('Time')
        df = df['2016-10-01':'2017-10-01']
        print(service_name,df.head(),df.tail())
        Interval = list(df['Interval'])
        print("max",max(Interval))
        Interval = deleteZero(Interval)

        # Price, Interval = Zscore(Price, Interval)
        # Interval = stats.zscore(Interval)
        fo.write(file_name[0] + ",")
        fo.write((str)(GlobalStatistic(Interval)))
        fo.write("\n")

fo.close()
