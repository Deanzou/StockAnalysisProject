import os

import datetime
import numpy as np
import pandas as pd

filedir =  'PycharmProjects/StockAnalysis/StockAnalysis/'
filename = 'data/HKEXSearchCach00700/brokers_postion_00700.csv'
fdpos = pd.read_csv(filedir+filename, index_col=0, parse_dates=True)

from pylab import mpl
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontManager, FontProperties

plt.rcParams['font.family'] = ['PingFang']

def getChineseFont():
    return FontProperties(fname='/System/Library/Fonts/PingFang.ttc')


def timeParse(strtimedate):
    return datetime.datetime.strptime(strtimedate,'%Y年%m月%d日')
stockprice = pd.read_csv( filedir+'data/騰訊控股歷史數據.csv', index_col=0, parse_dates=True, infer_datetime_format=True, date_parser=timeParse)

result = stockprice.join(fdpos)
result.tail()


%matplotlib qt5


timeperiod = 30
plt.title(u"持仓情况分析", fontproperties=getChineseFont())
ax1 = plt.subplot()
ax1.plot(result['最新'].iloc[0:timeperiod], c='r', label='700')
ax1.legend(loc=2)
ax1.grid(False)
ax2 = ax1.twinx()
ax2.plot(result['B01451'].iloc[0:timeperiod], c='b', label=u"高盛")
ax2.legend(loc=1)
plt.rc('font', family=['PingFang'])
plt.show()

txclose.resample('Q').apply(lambda x : x[-1]/x[0]-1)