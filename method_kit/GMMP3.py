import datetime
import re
import matplotlib
matplotlib.use('Agg')
import seaborn as sns
sns.set(style = "white")
from sklearn import mixture
import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as stats
import numpy as np
from numpy import *
from statistics import *
import matplotlib.cm as cmx
import matplotlib.colors as colors
import matplotlib as mpl
from matplotlib import cm
import itertools
import time

dataname = ['Type', 'OS', 'Region', 'Time', 'Price', 'Interval']
# Windows # SUSE Linux (Amazon VPC)
filepath = '/Users/lixuefei/Desktop/SCC2018/test/c1.medium_Linux-UNIX_us-east-1a.txt' #'2month
df = pd.read_table(filepath,names = dataname)

df = df.drop(['Type', 'OS', 'Region'],axis = 1)
df['Time'] = pd.to_datetime(df['Time'])
df = df.set_index('Time')
df = df['2016-10-01':'2017-10-01']
print(df)
print(max(df['Interval']))
# X = data[['Price']]#,'Interval']]#.sample(n=50)#frac = 0.1)
# bic = []
# n_components_range = range(2,5)

# fit model
# lowest_bic = np.infty
# cv_types = ['spherical', 'tied', 'diag', 'full']
# for cv_type in cv_types:
#     for n in n_components_range:
#         # gmm = mixture.BayesianGaussianMixture(n_components=n,covariance_type=cv_type).fit(X)
#
#         bictemp = gmm.bic(X)
#         print(n,bictemp)
#         bic.append(bictemp)
#         if bic[-1] < lowest_bic:
#             lowest_bic = bic[-1]
#             best_gmm = gmm
#             best_cv = cv_type
#             best_n = n
# print(best_cv,best_n,lowest_bic)
# min = df['Interval'].min()

min = math.ceil(min(df['Price']))
Dist = []
mode = mode(df['Interval'])
print("mode is",mode)
for i in range(len(df)):
    # print("yes!",df.iloc[i]['Interval'])
    times = int(df.iloc[i]['Interval'] / mode)
    Dist.extend(df.iloc[i]['Price'].repeat(times))
    # print(i/len(df))
Dist = np.array(Dist).reshape(-1,1)
# print(Dist)


gmm = mixture.GaussianMixture(n_components = 3)#,covariance_type= 'full')
gmm.fit(Dist)# diag full 2 比较好

# labels = gmm.predict(Dist)
index = np.arange(0,len(Dist),1)
# plt.scatter(index, Dist, c = labels,cmap = 'brg',s=40,alpha = 0.4,marker = '8',linewidth = 0)#,cMAP
print("test")
indexList = np.arange(0,len(Dist),1)
data = pd.DataFrame(index = indexList).reset_index()
data['Price'] = Dist
data['Label']= gmm.predict(Dist)
data['Number'] = np.arange(0,len(Dist),1)
# # X['Time'] = data.index
data.reset_index()
# print(data)

#plot and save figure
fig1 = plt.figure(1,figsize=(6,4))

colors = ['b','g','r']#,'orange']
Label_Com = ['Component 1','Component 2','Component 3']#,'Component 4']
for index in range(3):
    Price = data.loc[data['Label'] == index]['Price']
    # Price = Dist[Labels[i] == index]
    Index = data.loc[data['Label'] == index]['Number']
    print("Done")
    # 1475251200 20161001
    # timestamp = 1475251200
    # Index = timestamp + Index
    # print(Index)
    # time_local = time.localtime(Index)
    # Index = time.strftime("%Y-%m-%d %H:%M:%S",time_local)

    plt.scatter(Index, Price, c=colors[index], cmap='brg', s=40, alpha=0.2, marker='8', linewidth=0)  # ,cMAP

# for i in range(0,len())
plt.ylim(0.01,0.09)
plt.xticks([])
plt.xlabel('Time',fontsize = 20)
plt.ylabel('Price',fontsize = 20)
plt.yticks(fontsize = 20)
ax = fig1.gca()
# x 轴不可见
# ax.axes.get_xaxis().set_visible(False)
for label in ax.xaxis.get_ticklabels():
    label.set_rotation(30)
#added this to get the legend to work
handles,labels = ax.get_legend_handles_labels()
ax.legend(handles, labels = Label_Com, loc='upper right',fontsize = 18 )

# ax.grid()
# plt.show()
plt.tight_layout()
plt.savefig('/Users/lixuefei/Desktop/SCC2018/GMMP20180602three.png',dpi = 1500)

plt.close()


