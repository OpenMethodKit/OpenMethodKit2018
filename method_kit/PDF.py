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
    meanP, meanI,stdP,stdI   = WmeanStd(data)
    for i in range(len(data)):
        ZP = (data['Price'][i] - meanP)/ stdP
        ZI = (data['Interval'][i] - meanI)/ stdI
        if(ZP>3 or ZP<-3 or ZI > 3 or ZI < -3):
            data.drop(i, inplace=True)
    return data

dataname = ['Type', 'OS', 'Region', 'Time', 'Price', 'Interval']
path = '/Users/lixuefei/Desktop/SCC2018/test/c1.medium_Linux-UNIX_us-east-1a.txt'#c1.medium_Linux-UNIX_us-east-1c
df = pd.read_table(path,names = dataname)# header = None,
df = df.drop(['Type', 'OS', 'Region'], axis=1)
df['Time'] = pd.to_datetime(df['Time'])
df = df.set_index('Time')
df = df['2016-10-01':'2017-10-01']
print(df)
# df = df.groupby('Price').sum()
df = Zscore(df)
min = math.ceil(min(df['Price']))
max = math.floor(max(df['Price']))

fig = plt.figure(1,figsize=(8,8))

Dist = []
for i in range(len(df)):
    print("yes!",df.iloc[i]['Interval'])
    times = df.iloc[i]['Interval']/min
    Dist.extend(df.iloc[i]['Price'].repeat(times))
    print(i/len(df))
Dist = np.array(Dist)
print(Dist)

ax1 = plt.gca()  # 获取当前图像的坐标轴信息
# plt.title('Probability density function')
#ax1.yaxis.get_major_formatter().set_powerlimits((0,1)) # 将坐标轴的base number设置为一位。
# new_ticks = np.linspace(min, max, 5)
# ax1.set_xticks(new_ticks)
# plt.hist(Dist, color = 'r',alpha = 0.5,histtype="stepfilled")
sns.distplot(Dist,hist=True, color = 'brown',kde=True,
             kde_kws={'linewidth':3},
             hist_kws={'color':'b'})#,alpha = 0.5)#, linewidth = 0)#,hist=True)

# sns.kdeplot(Dist)

# plt.hist(Dist, color = 'r')
#sns.distplot(Dist,kde = False)
# 设置刻度字体大小
plt.xticks(fontsize=26)
plt.yticks(fontsize=26)
# plt.xlim(-1,4)
# plt.ylim(0,270)
# 设置坐标标签字体大小
ax1.set_xlabel(xlabel='Price($/hour)', fontsize=26)
ax1.set_ylabel(ylabel='Probability Density', fontsize=26)

for ind, label in enumerate(ax1.xaxis.get_ticklabels()):
    if ind % 2 == 0:  # every 10th label is kept
        label.set_visible(True)
    else:
        label.set_visible(False)

plt.show()


plt.tight_layout()
plt.savefig('/Users/lixuefei/Desktop/SCC2018/PDF20180531.pdf')#,dpi = 1500)



