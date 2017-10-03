import ExchangeRateAnalysis as exrate
import pandas as pd
import pandas_datareader.data as web
import datetime as dt
import numpy as np

datapath = './data/txprice.xls'
reportpath = './data/txfinacial.xls'

def getTXPriceFromYahoo(start=dt.datetime(2008,1,1), end=dt.datetime.today()) :
    txprice = web.DataReader("0700.HK", 'yahoo', start, end)
    return txprice


#保存近10年的数据到excel
def saveTxPrice2Excel():
    txprice = pd.DataFrame()
    print('get 700 price data from yahoo/n')
    txprice = getTXPriceFromYahoo()
    print(txprice)
    txprice.to_excel(datapath, sheet_name='TENCENT')
    return txprice

#从保存文件中读取
def readTxPricefromExcel():
    txprice = pd.read_excel(datapath, sheetname='TENCENT')
    print(txprice)
    return txprice

#获取股价
#           Date      Open      High       Low     Close  Adj Close  Volume
def getTxPrice():
    txprice = pd.DataFrame()
    needUpdate = True
    try:
        txprice = readTxPricefromExcel()
    except:
        print('read TxPrice error', datapath, '/n')
    else:
        enddate = txprice.iloc[-1, 0]
        if enddate >= datetime.today():
            needUpdate = False

    if needUpdate:
        print('update 700 price', datapath)
        try:
            txprice = saveTxPrice2Excel()
        except:
            print('update 700 price error', datapath)
        else:
            print('update 700 price data sucess!!!')
    return txprice

#读入财报相关数据
def readTxReport():

    #读取每个季度的数据
    txFirstQReports = pd.read_excel(reportpath, sheetname="第一季度业绩")
    txInterimReports = pd.read_excel(reportpath, sheetname="中期业绩")
    txTirdQReports = pd.read_excel(reportpath, sheetname="第三季度业绩")
    txAnnualReports = pd.read_excel(reportpath, sheetname="全年业绩")

    txFirstQReports["报告发布日期"] = np.nan
    txInterimReports["报告发布日期"] = np.nan
    txTirdQReports["报告发布日期"] = np.nan
    txAnnualReports["报告发布日期"] = np.nan

    #提取财报发布日期
    txReportNews = pd.read_excel(reportpath, sheetname='reportdate')
    txReportNewsSeries = txReportNews.iloc[:, 0]
    #根据每行字符串处理
    def processNews(news):
        datestr = news[0:10]
        date = dt.datetime.strptime(datestr, "%Y/%m/%d")

        idx = news.find("第一季度业绩公布")
        if idx >= 0:
            year = news[idx-5:idx-1]
            #idx = txFirstQReports.loc[txFirstQReports.业绩日期 == dt.datetime.strptime(year, "%Y")].index
            #txFirstQReports.iloc[idx, "报告发布日期"] = date

        return news
    txReportNewsSeries.apply(processNews)
    print(txFirstQReports)

    return


if __name__ == "__main__" :
    print('TxStockAnalysis.py __main__/n')

 #   txprice  = getTxPrice()
 #   print(txprice)
    readTxReport()