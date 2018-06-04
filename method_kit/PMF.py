# Plot CDF
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(style="white") #设置绘图背景
import math
pd.options.mode.chained_assignment = None  # default='warn'

# Change Time Interval correctly
def IntervalChange(data):
    for i in range(len(data)-1):
        data.ix[i,['Interval']] = int(data.ix[i+1, ['Interval']])
    data.ix[len(data)-1,['Interval']] = 0
    #data.convert_objects(convert_numeric=True) #dtype
    return data

def WmeanStd(data):
    # Weighted Mean price
    weightSum = np.sum(data['Price'] * data['Interval'])  # sum of weight:price * interval
    IntervalSum = np.sum(data['Interval'])  # Sum Interval
    meanP = weightSum / IntervalSum
    meanI = IntervalSum / len(data)

    # std
    stdI = np.std(data['Interval'])
    sum = 0
    for i in range(len(data)):
        sum += np.power((((data.iloc[i]['Interval'] / meanI) * data.iloc[i]['Price']) - meanP), 2)
    stdP = np.sqrt(sum / (len(data) - 2))

    return meanP,meanI,stdP,stdI

def Zscore(data):
    # 删除离群点
    meanP, meanI, stdP, stdI = WmeanStd(data)
    for i in range(len(data)):
        ZP = (data['Price'][i] - meanP)/ stdP
        ZI = (data['Interval'][i] - meanI)/ stdI
        if(ZP>3 or ZP<-3 or ZI > 3 or ZI < -3):
            data.drop(i, inplace=True)
    return data

dataname = ['Type', 'OS', 'Region', 'Time', 'Price', 'Interval']
df = pd.read_table('/Users/lixuefei/Desktop/SCC2018/test/c1.medium_Linux-UNIX_us-east-1a.txt',names = dataname).round(3)#c1.medium us-east-1c
# header = None,

df = IntervalChange(df)
df = Zscore(df)

df.sort_values(by = 'Price')# 按价格排序

# Dist = []
Price = []
df = df.groupby('Price')
for price, group in df:
    Price.append(price)
    # Dist.extend(np.repeat(price,group['Interval'].sum()))
    # print(price,  group['Interval'].sum())
df = df.sum()
df['Interval'] /= df['Interval'].sum()

print(df['Interval'])
plt.figure(1,figsize=(5.58,4))

#df.plot(kind='bar', width = 0.5, linewidth = 0,legend = None)
plt.bar(left=np.arange(len(df)),height=df['Interval'],width = 0.6) #, width=0.3 ,align='center', color='y',linewidth = 1)#, fit=stats.gamma)

# 设置刻度字体大小
plt.xticks(np.arange(len(df)),Price,fontsize=12)
plt.yticks(fontsize=12)

plt.xlim(0,20)
# plt.ylim(0,0.22)
# plt.title("Probability mass function",fontsize = 16)
ax1 = plt.gca()  # 获取当前图像的坐标轴信息
# 设置坐标标签字体大小
ax1.set_xlabel(xlabel='Price($/hour)', fontsize=12)
ax1.set_ylabel(ylabel='Probability', fontsize=12)

# for ind, label in enumerate(ax1.xaxis.get_ticklabels()):
#     if ind % 2 == 0:  # every 10th label is kept
#         label.set_visible(True)
#     else:
#         label.set_visible(False)

# plt.show()

for label in ax1.xaxis.get_ticklabels():
    label.set_rotation(90)

plt.tight_layout()
plt.savefig('/Users/lixuefei/Desktop/SCC2018/PMF20180429.pdf')#,dpi = 1500)



