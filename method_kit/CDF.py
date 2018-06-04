# Plot CDF
from statistics import *
from numpy import *

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(style="white") #设置绘图背景
import pandas as pd
import numpy as np
pd.options.mode.chained_assignment = None  # default='warn'
pd.set_option('precision', 2)
import os

def Zscore(data):
    # 删除离群点
    meanP = mean(data['Price'])
    meanI = mean(data['Interval'])
    stdP = std(data['Price'])
    stdI = std(data['Interval'])

    for i in range(len(data)):
        ZP = (data['Price'][i] - meanP)/ stdP
        ZI = (data['Price'][i] - meanI)/ stdI
        if(ZP>3 or ZP<-3 or ZI > 3 or ZI < -3):
            data.drop(i, inplace=True)
    return data
maxprice = 2.2

def draw_CDF(df,c,label):
    # df = IntervalChange(df)
    df_sort = df.sort_values(by=['Price'])
    # df_sort.sample(frac = 0.01) #太多展示结果太密集 还没有好的办法 或者去掉x轴

    df_sort = df_sort.round(4)
    SI = np.sum(df_sort['Interval'])
    sum = df_sort.iloc[0]['Interval']
    AccumulateInterval = []
    AccumulateInterval.append(df_sort.iloc[0]['Interval'] / SI)
    for i in range(1, len(df_sort)):
        sum += df_sort['Interval'][i]
        AccumulateInterval.append(sum / SI)
    #print(AccumulateInterval)
    price = list(df_sort['Price'])

    price.append(maxprice)
    AccumulateInterval.append(1)

    plt.plot(price, AccumulateInterval,color = c ,label = label)#linestyle = '-',marker = '+',)
    ax = plt.gca()
    # 设置刻度字体大小
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    plt.ylim(0, 1.1)
    plt.xlim(0, maxprice)
    # 设置坐标标签和字体大小
    ax.set_xlabel(xlabel='Price($/hour)', fontsize=20)
    ax.set_ylabel(ylabel='Availability', fontsize=20)

# 定义文件夹
datapath = '/Users/lixuefei/Desktop/SCC2018/CDF'
# 抽取数据所在的文件列表
filelist = os.listdir(datapath)
# 定义列表名称
dataname = ['Type', 'OS', 'Region', 'Time', 'Price', 'Interval']
color = ['darkorange','darkblue','darkgreen','blue','darkred','yellow']
x = 0
fig = plt.figure(1, figsize=(6, 4))

def read_table(path):
    df = pd.read_table(path, names=dataname)
    df = df.drop(['Type', 'OS', 'Region'], axis=1)
    df['Time'] = pd.to_datetime(df['Time'])
    df = df.set_index('Time')
    df = df['2016-10-01':'2017-10-01']

    return df



# df1 = pd.read_table('/Users/lixuefei/Desktop/SCC2018/CDF/Linux-UNIX.txt', names=dataname)  # c1.mediumSUSE Linux (Amazon VPC)us-east-1a header = None,
# df2 = pd.read_table('/Users/lixuefei/Desktop/SCC2018/CDF/SUSE Linux (Amazon VPC).txt', names=dataname)  # c1.mediumSUSE Linux (Amazon VPC)us-east-1a header = None,
# df3 = pd.read_table('/Users/lixuefei/Desktop/SCC2018/CDF/Linux-UNIX (Amazon VPC).txt', names=dataname)  # c1.mediumSUSE Linux (Amazon VPC)us-east-1a header = None,
# df4 = pd.read_table('/Users/lixuefei/Desktop/SCC2018/CDF/Windows.txt', names=dataname)  # c1.mediumSUSE Linux (Amazon VPC)us-east-1a header = None,
# df5 = pd.read_table('/Users/lixuefei/Desktop/SCC2018/CDF/Windows (Amazon VPC).txt', names=dataname)  # c1.mediumSUSE Linux (Amazon VPC)us-east-1a header = None,

df1 = read_table('/Users/lixuefei/Desktop/SCC2018/CDF/Linux-UNIX.txt')
df2 = read_table('/Users/lixuefei/Desktop/SCC2018/CDF/SUSE Linux (Amazon VPC).txt')
df3 = read_table('/Users/lixuefei/Desktop/SCC2018/CDF/Linux-UNIX (Amazon VPC).txt')
df4 = read_table('/Users/lixuefei/Desktop/SCC2018/CDF/Windows.txt')
df5 = read_table('/Users/lixuefei/Desktop/SCC2018/CDF/Windows (Amazon VPC).txt')

draw_CDF(df1,color[0],'Linux-UNIX')
draw_CDF(df2,color[1],'SUSE Linux (Amazon VPC)')
draw_CDF(df4,color[4],'Windows')
draw_CDF(df3,color[2],'Linux-UNIX (Amazon VPC)')
draw_CDF(df5,color[3],'Windows (Amazon VPC)')

ax = plt.gca()
handles,labels = ax.get_legend_handles_labels()
print(handles,labels)

handles = [handles[0], handles[2], handles[1],handles[3], handles[4]]
labels = [labels[0], labels[2], labels[1], labels[3], labels[4]]

plt.legend(handles,labels,bbox_to_anchor=(1.0,0.6),fancybox=True,fontsize = 16)
plt.tight_layout()
plt.savefig('/Users/lixuefei/Desktop/SCC2018/CDF20180531.pdf')#,dpi = 1500)
plt.close()