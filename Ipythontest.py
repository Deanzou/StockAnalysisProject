import os

import datetime
import numpy as np
import pandas as pd

pd.core.common.is_list_like = pd.api.types.is_list_like
import pandas_datareader.data as web

import fix_yahoo_finance as yf
yf.pdr_override() # <== that's all it takes :-)

filedir =  'PycharmProjects/StockAnalysis/StockAnalysis/'
filename = 'data/HKEXSearchCach00700/brokers_postion_00700.csv'
fdpos = pd.read_csv(filedir+filename, index_col=0, parse_dates=True)



"""
从文件读取
"""
def readTxpricefromcsv():
    def timeParse(strtimedate):
        return datetime.datetime.strptime(strtimedate,'%Y年%m月%d日')
    return pd.read_csv( filedir+'data/騰訊控股歷史數據.csv', index_col=0, parse_dates=True, infer_datetime_format=True, date_parser=timeParse)

# download dataframe
# try:
#     stockprice = web.get_data_yahoo("0700.HK", start="2007-01-01")
# except Exception as e:
#     print(e)
#     #stockprice= readTxpricefromcsv()
#     pass

stockprice= readTxpricefromcsv()
result = stockprice.join(fdpos)
result.tail()


%matplotlib qt5
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontManager, FontProperties

import seaborn as sns
sns.set(style="darkgrid")

def getChineseFont():
    return FontProperties(fname='/System/Library/Fonts/PingFang.ttc')


matplotlib.rcParams['font.sans-serif'] = 'WenQuanYi Micro Hei'

timeperiod = 30
plt.title(u"持仓情况分析", fontproperties=getChineseFont())
ax1 = plt.subplot(2,2,1)
ax1.plot(result['Close'].iloc[-timeperiod:], c='r', label='700')
ax1.legend(loc=2)
ax1.grid(False)
ax2 = ax1.twinx()
ax2.plot(result['B01451'].iloc[-timeperiod:], c='b', label=u"高盛")
#ax2.plot(result['B01274'].iloc[-timeperiod:], c='b', label=u"MORGAN STANLEY HONG KONG SECURITIES LTD")
#ax2.plot(result['B01161'].iloc[-timeperiod:], c='b', label=u"UBS SECURITIES HONG KONG LTD")
#ax2.plot(result['B01955'].iloc[-timeperiod:], c='b', label=u"富途证券国际(香港)有限公司")
#ax2.plot(result['A00003'].iloc[-timeperiod:], c='b', label=u"中国证券登记结算有限责任公司")
ax2.legend(loc=1)

ax1 = plt.subplot(2,2,2)
ax1.plot(result['Close'].iloc[-timeperiod:], c='r', label='700')
ax1.legend(loc=2)
ax1.grid(False)
ax2 = ax1.twinx()
#ax2.plot(result['B01451'].iloc[-timeperiod:], c='b', label=u"高盛")
#ax2.plot(result['B01274'].iloc[-timeperiod:], c='b', label=u"MORGAN STANLEY HONG KONG SECURITIES LTD")
#ax2.plot(result['B01161'].iloc[-timeperiod:], c='b', label=u"UBS SECURITIES HONG KONG LTD")
ax2.plot(result['B01955'].iloc[-timeperiod:], c='b', label=u"富途证券国际(香港)有限公司")
#ax2.plot(result['A00003'].iloc[-timeperiod:], c='b', label=u"中国证券登记结算有限责任公司")
ax2.legend(loc=1)

ax1 = plt.subplot(2,2,3)
ax1.plot(result['Close'].iloc[-timeperiod:], c='r', label='700')
ax1.legend(loc=2)
ax1.grid(False)
ax2 = ax1.twinx()
#ax2.plot(result['B01451'].iloc[-timeperiod:], c='b', label=u"高盛")
#ax2.plot(result['B01274'].iloc[-timeperiod:], c='b', label=u"MORGAN STANLEY HONG KONG SECURITIES LTD")
#ax2.plot(result['B01161'].iloc[-timeperiod:], c='b', label=u"UBS SECURITIES HONG KONG LTD")
#ax2.plot(result['B01955'].iloc[-timeperiod:], c='b', label=u"富途证券国际(香港)有限公司")
ax2.plot(result['A00003'].iloc[-timeperiod:], c='b', label=u"中国证券登记结算有限责任公司")
ax2.legend(loc=1)

ax1 = plt.subplot(2,2,4)
ax1.plot(result['Close'].iloc[-timeperiod:], c='r', label='700')
ax1.legend(loc=2)
ax1.grid(False)
ax2 = ax1.twinx()
#ax2.plot(result['B01451'].iloc[-timeperiod:], c='b', label=u"高盛")
ax2.plot(result['B01274'].iloc[-timeperiod:], c='b', label=u"MORGAN STANLEY HONG KONG SECURITIES LTD")
#ax2.plot(result['B01161'].iloc[-timeperiod:], c='b', label=u"UBS SECURITIES HONG KONG LTD")
#ax2.plot(result['B01955'].iloc[-timeperiod:], c='b', label=u"富途证券国际(香港)有限公司")
#ax2.plot(result['A00003'].iloc[-timeperiod:], c='b', label=u"中国证券登记结算有限责任公司")
ax2.legend(loc=1)

plt.show()

txclose.resample('Q').apply(lambda x : x[-1]/x[0]-1)


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
