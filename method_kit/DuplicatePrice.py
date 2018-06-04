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

def deleteSamePrice(Price,Interval):
    index = len(Price) - 1
    current_price = Price[index]
    sum_of_time = Interval[index]

    ResultP = []
    ResultI = []

    index = index - 1
    while (index >= 0):
        price = Price[index]
        interval = Interval[index]
        if(price == current_price):#.__dict__):#.__dict__
            sum_of_time += interval
        else:
            if(sum_of_time != 0):
                ResultP.append(round(current_price,4))
                ResultI.append(round(sum_of_time,4))
                current_price = price
                sum_of_time = interval

        index = index - 1
    if(sum_of_time!=0):
        print()
        ResultP.append(price)
        ResultI.append(interval)
    print("test1")
    for i in range(len(ResultI)):
        if(ResultI == 0):
            print("Found", i )
    return Price,Interval

def Zscore(Price,Interval):
    Interval = np.array(Interval)
    Price = np.array(Price)

    # meanI = Interval.sum() / (len(Interval) - 1)
    # Weighted Mean price
    meanP = (Price * Interval).sum() / Interval.sum()
    # print("mean",meanP)#meanI
    # std
    stdI = Interval.std()
    stdP = np.sqrt(np.sum(np.power((Price - meanP),2)*Interval) / Interval.sum())
    # print("std",stdI,stdP)
    ZP = (Price - meanP) / stdP
    # ZI = (Interval - meanI) / stdI

    ResultP = []
    ResultI = []
    for i in range(len(ZP)):

        if (ZP[i] > 3 or ZP[i] < -3 or Interval[i] == 0.0):# or ZI[i] > 3 or ZI[i] < -3):
            # print("no",Interval[i],Price[i],ZP[i])#, ZI[i])
            continue
        else:
            # print("yes",Interval[i],Price[i],ZP[i])#, ZI[i])
            ResultP.append(Price[i])
            ResultI.append(Interval[i])


    return ResultP,ResultI

def GlobalStatistic(Price, Interval):
    #
    Price = list(df['Price'])
    Interval = list(df['Interval'])

    # # mode
    # df = DataFrame()
    # df['Interval'] = Interval
    # df['Price'] = Price
    modeP = df['Price'][argmax(df['Interval'])]
    # print("mode",modeP)
    modeI = mode(df['Interval'])
    Interval = np.array(Interval)
    Price = np.array(Price)

    lenI = len(Interval)
    lenP = len(Price)
    # print(Interval.sort())
    # print(Price)
    if lenI == lenP:
        # max min
        maxInterval = max(Interval)
        minInterval = min(Interval)
        minPrice = min(Price)
        maxPrice = max(Price)
        # print(minInterval,maxInterval,minPrice,maxPrice)

        meanI = Interval.sum() / (lenI - 1)
        # Weighted Mean price
        meanP = (Price * Interval).sum() / Interval.sum()
        # print(meanI,meanP)

        # zscore

        # std
        stdI = Interval.std()
        stdP = np.sqrt(np.sum(np.power((Price - meanP),2)*Interval) / Interval.sum())
        print("std",stdP)

        CVI = stdI / meanI
        CVP = stdP / meanP
        # print(CVI,CVP)

        skewI = np.sum(np.power((Interval - meanI),3)) / (lenI * np.power(stdI,3))
        skewP = np.sum(np.power(Price - meanP,3) * Interval) / (np.power(stdP , 3)*Interval.sum())
        # print("test",skewI, skewP)

        kurtI = np.sum(np.power(Interval - meanI,4)) / (lenI * np.power(stdI,4)) - 3
        # print(np.sum(np.power(Interval - meanI,4)) ,"and", (lenI * np.power(stdI,4)) - 3)
        kurtP = np.sum(np.power(Price - meanP,4) * Interval) / (np.power(stdP,4)*Interval.sum()) - 3
        # print(np.sum(np.power(Price - meanP,4) * Interval) ,"and", (np.power(stdP,4)*Interval.sum()) - 3)
        # print("test",kurtI, kurtP)
        result = [minPrice,maxPrice,meanP,modeP,stdP,CVP,skewP,kurtP]
        result = [("%.4f" % i) for i in result]
        # print(result)
    return result
# 定义文件夹
datapath = '/Users/lixuefei/Desktop/Class'

# 抽取数据所在的文件列表
filelist = os.listdir(datapath)
# 定义列表名称
dataname = ['Type', 'OS', 'Region', 'Time', 'Price', 'Interval']

fo = open("fooPrice.csv", "w")
fo.write("name,minPrice,maxPrice,meanP,modeP,stdP,CVP,skewP,kurtP\n")

for files in filelist:
    file_name = os.path.splitext(files)  # 获取切片好的文件名
    if file_name[1] == '.txt':
        # 数据文件的地址
        cpath = os.path.join(datapath, files)
        service_name = file_name[0]
        print(service_name)
        df = pd.read_table(cpath,names=dataname)
        df = df.drop(['Type', 'OS', 'Region'],axis = 1)
        df['Time'] = pd.to_datetime(df['Time'])
        df = df.set_index('Time')
        df = df['2016-10-01':'2017-10-01']
        print("df",df.head(),df.tail())
        Price = list(df['Price'])
        Interval = list(df['Interval'])

        Price, Interval = deleteSamePrice(Price, Interval)
        Price, Interval = Zscore(Price, Interval)

        fo.write(file_name[0] + ",")
        fo.write((str)(GlobalStatistic(Price, Interval)))
        fo.write("\n")

fo.close()
