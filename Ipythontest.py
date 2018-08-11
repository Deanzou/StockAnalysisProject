import os

import datetime
import numpy as np
import pandas as pd
import math

pd.core.common.is_list_like = pd.api.types.is_list_like
import pandas_datareader.data as web

import fix_yahoo_finance as yf
yf.pdr_override() # <== that's all it takes :-)

filedir =  'PycharmProjects/StockAnalysis/StockAnalysis/'
filename = 'data/HKEXSearchCach00700/brokers_postion_00700.csv'
fdpos = pd.read_csv(filedir+filename, index_col=0, parse_dates=True)


#
# """
# 从文件读取
# """
# def readTxpricefromcsv():
#     def timeParse(strtimedate):
#         return datetime.datetime.strptime(strtimedate,'%Y年%m月%d日')
#     return pd.read_csv( filedir+'data/騰訊控股歷史數據.csv', index_col=0, parse_dates=True, infer_datetime_format=True, date_parser=timeParse)

# download dataframe
# try:
#     stockprice = web.get_data_yahoo("0700.HK", start="2007-01-01")
# except Exception as e:
#     print(e)
#     #stockprice= readTxpricefromcsv()
#     pass

stockprice = pd.read_csv(filedir+'data/HKEXSearchCach00700/stock_price_0700.HK.csv', index_col=0, parse_dates=True)
result = stockprice.join(fdpos)
result.tail()

dfReportsDates = pd.read_csv(filedir+'data/HKEXSearchCach00700/700ReportsDate.csv', index_col=0, parse_dates=True)


%matplotlib qt5
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontManager, FontProperties

import seaborn as sns
sns.set(style="darkgrid")

def getChineseFont():
    return FontProperties(fname='/System/Library/Fonts/PingFang.ttc')


matplotlib.rcParams['font.sans-serif'] = 'WenQuanYi Micro Hei'

dicBrokers = {'B01451':u"高盛",
              'B01274':u"MORGAN STANLEY",
              'B01161':u"UBS HK",
              'C00100':u"JPMORGAN",
              'B01121':u"法兴 HK",
              'A00003':u"中国证券登记结算有限责任公司",
              'C00019':u"汇丰",
              'C00039':u"渣打",
              'B01130':u"中银国际",
              'B01955':u"富途",
              }

timeperiod = 100
reportdates = dfReportsDates[(dfReportsDates.index >= result.index[-timeperiod]) &
                             (dfReportsDates.index <= result.index[-1])]
fig, axs = plt.subplots(math.ceil(len(dicBrokers)/2),ncols=2,figsize=(10,10),sharex=True)
plt.title(u"大行持仓", fontproperties=getChineseFont())
row = 0
col = 0
idx = 0
for key, name in dicBrokers.items():
    axs[row][col].plot(result['Close'].iloc[-timeperiod:], c='r', label='700')
    axs[row][col].legend(loc=2)
    #axs[row][col].grid(False)
    axs[row][col].set_title(name)
    ax2 = axs[row][col].twinx()
    ax2.plot(result[key].iloc[-timeperiod:], c='b')
    #画财报日期
    for day in reportdates.index:
        delta = (day - result.index[-timeperiod])/(result.index[-1]-result.index[-timeperiod])
        #axs[row][col].axvline(x=delta)
        axs[row][col].fill_between([day], axs[row][col].get_ylim()[0], axs[row][col].get_ylim()[1], color='r',
                                   linestyle='--',lw=2)

    #ax2.legend(loc=1)
    idx+=1
    col = idx % 2
    row = idx // 2


plt.show()


#txclose.resample('Q').apply(lambda x : x[-1]/x[0]-1)


"""
读取股票数据
"""

import pandas as pd
pd.core.common.is_list_like = pd.api.types.is_list_like
import pandas_datareader.data as web
import datetime

import fix_yahoo_finance as yf
yf.pdr_override() # <== that's all it takes :-)

# download dataframe
data = web.get_data_yahoo("0700.HK", start="2017-01-01", end="2017-04-30")

# download Panel
data = web.get_data_yahoo(["SPY", "IWM"], start="2017-01-01", end="2017-04-30")


"""
股价分析
"""
