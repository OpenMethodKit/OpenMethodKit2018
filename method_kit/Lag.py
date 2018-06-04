# Plot Lag
import time
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from pandas.plotting import lag_plot
import seaborn as sns
import pypdftk
import numpy as np
sns.set(style="white") #设置绘图背景

pd.options.mode.chained_assignment = None  # default='warn'
pd.set_option('precision', 2)

#cg1.4xlarge_Windows_us-east-1c
#c1.medium_Windows_us-east-1c
#c1.medium_Linux-UNIX_us-east-1a
dataname = ['Type', 'OS', 'Region', 'Time', 'Price', 'Interval']
df = pd.read_table('/Users/lixuefei/Desktop/SCC2018/test/c1.medium_Linux-UNIX_us-east-1a.txt',names = dataname)# c1.mediumSUSE Linux (Amazon VPC)us-east-1a header = None,
df = df.drop(['Type', 'OS', 'Region'], axis=1)
# df['Time'] = pd.to_datetime(df['Time'])
# df = df.set_index('Time')
# df = df['2016-10-01':'2017-10-01']
#fig = plt.figure(1,figsize=(7,7))

# Get timestamp


# StartTime = time.strptime(df.iloc[0,['Time']], "%Y-%m-%dT%H:%M:%S")
# StartTimeStamp = int(time.mktime(StartTime))
StartTimeStamp = 1475251200 #2016-10-01
# EndTime = time.strptime(df['Time'][len(df)-1][:19], "%Y-%m-%dT%H:%M:%S")
# EndTimeStamp = int(time.mktime(EndTime))
EndTimeStamp = 1506787200

TimeList = []
for t in range(len(df)):
    Time = time.strptime(df['Time'][t][:19], "%Y-%m-%dT%H:%M:%S")
    TimeStamp = int(time.mktime(Time))
    TimeList.append(TimeStamp)
#print(TimeList)

Interval = 60*60*1

TimeListCur = []
PriceOri = []
PriceCur = []

tip = 0

def findInterval(timestamp):
    for i in range(len(TimeList)):
        if(TimeList[i] < timestamp and TimeList[i+1] > timestamp):
            #print("found")
            return i


index = 0

for i in range(len(TimeList)):
    #print("List",TimeList[i])
    currentTime = TimeList[i] + Interval
    if(currentTime > EndTimeStamp):
        break
    if(TimeList.__contains__(currentTime)):
        #print("have this timestamp")
        index = TimeList.index(currentTime)

        PriceOri.append(df['Price'][i])
        PriceCur.append(df['Price'][index])

    else:
        print("don`t have this timestamp")
        PriceCur.append(df['Price'][findInterval(currentTime)])

        PriceOri.append(df['Price'][i])

fig = plt.figure(1,figsize=(7,7))

plt.scatter(PriceOri,PriceCur,alpha=0.2,c='#0099CC')#,linewidths=0.3

ax1 = plt.gca()  # 获取当前图像的坐标轴信息

# 设置刻度字体大小
plt.xticks(fontsize=24)
plt.yticks(fontsize=24)

# 设置坐标标签字体大小
ax1.set_xlabel(xlabel='Price at time T ($/hour)', fontsize=24)
ax1.set_ylabel(ylabel='Price at time T+1 hour ($/hour)', fontsize=24)

plt.tight_layout()
#plt.show()
plt.savefig('/Users/lixuefei/Desktop/SCC2018/LAG1h20180531.png',dpi = 1200)

plt.close()
#
#
#
#
#
#
# TimeInterval = int((EndTimeStamp - StartTimeStamp)/3600*3) #
# TimeInterval = 60 * 60
# fig1 = plt.figure(1)
# pLag = lag_plot(df['Price'],lag = TimeInterval, alpha=0.2, linewidths=0.3)
# min = min(df['Price'])
# max = max(df['Price'])
#
# ax1 = plt.gca()  # 获取当前图像的坐标轴信息
#
# #ax1.set_xticks([min,(min+max)/2,max])
# #ax1.set_yticks([0,0.5,1])
#
# # plt.xlim((min-0.01, min+0.01))
# # plt.ylim((min-0.01, min+0.01))
#
#
# # ax1 = plt.gca()  # 获取当前图像的坐标轴信息
# # plt.tight_layout()
# # ax1.set(xlabel='', ylabel='')
# # 设置刻度字体大小
# plt.xticks(fontsize=24)
# plt.yticks(fontsize=24)
#
# # 设置坐标标签字体大小
# ax1.set_xlabel(xlabel='Price at time T ($/hour)', fontsize=24)
# ax1.set_ylabel(ylabel='Price at time T+0.5 hour ($/hour)', fontsize=24)
# plt.show()
#
#
