cd PycharmProjects/StockAnalysis/StockAnalysis/


import StockHisData
import HKEXNewsHoldingAnalysis

import pandas as pd
import numpy as np

stockdata = StockHisData.StockHisData(HKEXNewsHoldingAnalysis.searchHtmlCatchPath,"0700.HK")
stockdata.load_csv()

stockdata.stockprice['Return'] = np.log(stockdata.stockprice['Adj Close']/stockdata.stockprice['Adj Close'].shift(1))
price = stockdata.stockprice

signaldays = price[(price['Return']>0.02)|(price['Return']<-0.02)]
signaldays1mask = (price['Return']>0.02)|(price['Return']<-0.02)
signaldays1mask = signaldays1mask.shift(1)
signaldays1 = price[signaldays1mask==True]

row = pd.DataFrame({}, index=pd.DatetimeIndex(["2018-08-03"]))
signaldays1.append(row)


signaldays['Return1']=signaldays1['Return'].values

