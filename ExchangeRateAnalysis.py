
import numpy as np
import pandas as pd
import pandas_datareader.data as web
from datetime import datetime

datapath = './data/exchangerate.xls'

#通过Yahoo查询汇率，网站不支持CNY／HKD需要通过美元转换
def getCNY2HKDFromYahoo(start, end):

    try:
        cny2usd = web.DataReader("CNY=X", 'yahoo', start, end)
        hkd2usd = web.DataReader("HKD=X", 'yahoo', start, end)
    except:
        print('getCNY2HKDFromYahoo error!')
    else:
        print('getCNY2HKDFromYahoo success!')

    return cny2usd / hkd2usd

#保存近10年的汇率数据到excel
def saveRate2Excel():
    cny2hkd = pd.DataFrame()
    print('get data from yahoo/n')
    cny2hkd = getCNY2HKDFromYahoo(datetime(2008, 1, 1), datetime.now())
    print(cny2hkd)
    cny2hkd.to_excel(datapath, sheet_name='CNY2HKD')
    return cny2hkd

#从保存文件中读取
def readRatefromExcel():
    cny2hkd = pd.read_excel(datapath, sheetname='CNY2HKD')
    print(cny2hkd)
    return cny2hkd

#获取汇率数据 pandas.DataFrame
#           Date      Open      High       Low     Close  Adj Close  Volume
#0    2007-12-31  0.934913  0.934853  0.935825  0.935501   0.935501     NaN
#1    2008-01-01  0.935501  0.934758  0.937461  0.935033   0.935033     NaN
#2    2008-01-02  0.933856  0.932255  0.934072  0.932565   0.932565     NaN
def getCNY2HKD():
    cny2hkd = pd.DataFrame()
    needUpdate = True
    try:
        cny2hkd = readRatefromExcel()
    except:
        print('read error', datapath, '/n')
    else:
        enddate = cny2hkd.iloc[-1, 0]
        delta = datetime.today()-enddate
        if delta.days <= 0:
            needUpdate = False
            print('don\'t need to update!')

    if needUpdate:
        print('update ', datapath)
        try:
            cny2hkd = saveRate2Excel()
        except:
            print('update error', datapath)
        else:
            print('update data success!!!')
    return cny2hkd





if __name__ == "__main__" :
    print('ExchangeRateAnalysis.py __main__/n')

    cny2hkd = getCNY2HKD()
    print(cny2hkd)