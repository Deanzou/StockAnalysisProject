# -*- coding: utf-8 -*-
"""
管理所有的文件，并汇总到DataFrame
"""
import os

import datetime
import pandas as pd

from HKEXBrokersPage import HKEXBrokersPage


import unittest


class HKEXNewsDatabase(object):

    def __init__(self, path, code):
        self.path = path
        self.df_id2names = pd.DataFrame()
        self.df_brokersPos = pd.DataFrame()
        self.code = code

    def process_allpages(self):
        for root, dirs, files in os.walk(self.path):
            for filepath in files:
                pagepath = os.path.join(self.path, filepath)
                if pagepath[-5:] == '.html':
                    print("HKEXBrokersPage(%s)"%pagepath)
                    try:
                        # 判断该日期的文件是否已经解析
                        date = datetime.datetime.strptime(filepath[0:8], '%Y%m%d')
                        if date in self.df_brokersPos.index:
                            continue
                        page = HKEXBrokersPage(pagepath)
                        self.df_brokersPos = self.df_brokersPos.append(page.get_brokersPostionDataFrame(), sort=True)
                        if self.code is None:
                            self.code = page.stock_code
                        assert self.code == page.stock_code
                    except Exception as e:
                        print(e)
                        self.save_csv('brokers_position_tmp_%s.csv'%filepath)

    def save_csv(self, filename =''):
        print('save_csv begin')
        if self.code is None:
            self.code = 'nonecode'
            print("process error stock code == None!!!!")

        if filename == '':
            filename = self.path + '/brokers_postion_%s.csv'%self.code
        else:
            filename = self.path + '/' + filename
        print(self.df_brokersPos)
        self.df_brokersPos.to_csv(filename)
        print('save_csv end')

    def load_csv(self,filename=''):
        print('load_csv begin')
        if self.code is None:
            self.code = 'nonecode'
            print("process error stock code == None!!!!")

        if filename == '':
            filename = self.path + '/brokers_postion_%s.csv'%self.code
        else:
            filename = self.path + '/' + filename

        fdpos = pd.read_csv(filename, index_col=0, parse_dates=True)
        self.df_brokersPos = pd.concat([self.df_brokersPos, fdpos])


# ***********************************************************************************************************************
"""
unittest
"""


class TestHKEXNewsDatabase(unittest.TestCase):
    def setUp(self):
        print("TestHKEXNewsDatabase::setUp begin")
        self.searchHtmlCatchPath = './data/HKEXSearchCach00700'
        self.database = HKEXNewsDatabase(self.searchHtmlCatchPath, '00700')

    def test_save_csv(self):
        try:
            self.database.load_csv()
        except Exception as e:
            print(e)
            pass

        self.database.process_allpages()
        self.database.save_csv()


if __name__ == '__main__':
    unittest.main()
