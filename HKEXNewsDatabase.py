#-*- coding: utf-8 -*-
"""
管理所有的文件，并汇总到DataFrame
"""
import os

import datetime
import numpy as np
import pandas as pd

from HKEXBrokersPage import HKEXBrokersPage


import unittest


class HKEXNewsDatabase(object):

    def __init__(self, path):
        self.path = path
        self.df_id2names = pd.DataFrame()
        self.df_brokersPos = pd.DataFrame()
        self.code = None

    def process_allpages(self):
        for root, dirs, files in os.walk(self.path):
            for filepath in files:
                pagepath = os.path.join(self.path, filepath)
                if pagepath[-5:] == '.html':
                    print("HKEXBrokersPage(%s)"%pagepath)
                    try:
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




# ***********************************************************************************************************************
"""
unittest
"""

class TestHKEXNewsDatabase(unittest.TestCase):
    def setUp(self):
        print("TestHKEXNewsDatabase::setUp begin")
        self.searchHtmlCatchPath = './data/HKEXSearchCach00700'
        self.database = HKEXNewsDatabase(self.searchHtmlCatchPath)

    def test_save_csv(self):
        self.database.process_allpages()
        self.database.save_csv()