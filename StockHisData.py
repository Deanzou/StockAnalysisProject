#-*- coding: utf-8 -*-
"""
#下载股价数据，存储至本地
"""
import os
import pandas as pd
import datetime

pd.core.common.is_list_like = pd.api.types.is_list_like
import pandas_datareader.data as web

#解决yahoo不能读取问题
import fix_yahoo_finance as yf
yf.pdr_override() # <== that's all it takes :-)

import HKEXNewsHoldingAnalysis

import unittest

class StockHisData:
    def __init__(self, home, code):
        self.home = home
        self.code = code
        self.stockprice = pd.DataFrame()

    def req_stockdata(self):
        # download dataframe
        try:
            self.stockprice = web.get_data_yahoo(self.code, start="2006-01-01")
        except Exception as e:
            print(e)

    def save_csv(self, filename =''):
        print('save_csv begin')
        if self.code is None:
            self.code = 'nonecode'
            print("process error stock code == None!!!!")

        if filename == '':
            filename = self.home + '/stock_price_%s.csv'%self.code
        else:
            filename = self.home + '/' + filename
        print(self.stockprice)
        self.stockprice.to_csv(filename)
        print('save_csv end')

    def load_csv(self,filename=''):
        print('load_csv begin')
        if self.code is None:
            self.code = 'nonecode'
            print("process error stock code == None!!!!")

        if filename == '':
            filename = self.home + '/stock_price_%s.csv'%self.code
        else:
            filename = self.home + '/' + filename

        fdprice = pd.read_csv(filename, index_col=0, parse_dates=True)
        self.stockprice = pd.concat([self.stockprice, fdprice])
        print('load_csv end')

    def update_stockprice(self, filename=''):
        print('update_csv begin')
        self.stockprice.sort_index(ascending=True)
        start = self.stockprice.index[-1].strftime("%Y-%m-%d")
        stockprice = pd.DataFrame()
        # download dataframe
        try:
            stockprice = web.get_data_yahoo(self.code, start=start)
            #print(stockprice)
            #print("update_stockprice:get_date_yahoo")
        except Exception as e:
            print(e)
            print('update_csv error!!!')

        self.stockprice = self.stockprice.append(stockprice)
        self.stockprice.drop_duplicates(inplace=True)
        print('update_csv end')

    def update_csv(self, filename=''):
        if filename == '':
            filepath = self.home + '/stock_price_%s.csv'%self.code
        else:
            filepath = self.home + '/' + filename
        if not os.path.exists(filepath):
            self.req_stockdata()
            self.save_csv()
        else:
            self.load_csv(filename)
            self.update_stockprice(filename)
            self.save_csv(filename)
"""
unittest
"""
class TestStockHisData(unittest.TestCase):
    def setUp(self):
        self.stockhisdata = StockHisData(HKEXNewsHoldingAnalysis.searchHtmlCatchPath, "0700.HK")

    def test_report(self):
        self.stockhisdata.update_csv()