#-*- coding: utf-8 -*-

"""
页面分析类
解析HKEXNews搜索结果页面
"""

import os

import datetime
import numpy as np
import pandas as pd

import bs4
import re

import unittest

class HKEXBrokersPage(object):

    def __init__(self, path):
        try:
            pageFile = open(path)
            assert pageFile
            self.soup = bs4.BeautifulSoup(pageFile, "lxml")
            self.brokers_id=[]
            self.brokers_name=[]
            self.brokers_postion={}
            self.brokers_address={}

            self.stock_code=''
            self.postion_date=datetime.datetime(1900,1,1)

            self.load_baseData()
            self.load_brokerslist()
        finally:
            pageFile.close()

    #获取页面持股信息/股份名称/代码
    def load_baseData(self):
        holdDateTitle = self.soup.find(text=re.compile("持股日期:"))
        holdDate = holdDateTitle.parent.find_next('td', attrs={"class": "arial12black", "nowrap": "nowrap"})
        holdDateText = holdDate.text.strip()  # 页面日期格式%D/%M/%Y
        self.postion_date = datetime.datetime.strptime(holdDateText, '%d/%m/%Y')

        stockCodeTitle = self.soup.find(text=re.compile("股份代号:"))
        stockCode = stockCodeTitle.parent.find_next('td', attrs={"class": "arial12black", "nowrap": "nowrap"})
        self.stock_code = stockCode.text.strip()

    #获取持股列表
    def load_brokerslist(self):
        tableParent = self.soup.select_one('#participantShareholdingList')
        # print(tableParent.tbody)

        table = tableParent.find_all('tr', re.compile("^row"))
        # print(table)
        for row in table:
            # print(row.contents[1].text)#参与者编号
            # print(row.contents[3].text)#中央结算系统参与者名称(*即愿意披露的投资者户口持有人)
            # print(row.contents[5].text)#地址
            # print(row.contents[7].text)#持股数量
            # print(row.contents[9].text)#占已发行股份/权证/单位百分比
            # 存入到名字id映射表中
            id = row.contents[1].text.strip().replace('\n', '')
            name = row.contents[3].text.strip().replace('\n', '')
            if id == '':
                id = name
            assert not id in self.brokers_id, '页面中参与者编号和名称不应该重复'
            self.brokers_id.append(id)
            self.brokers_name.append(name)
            # 经纪商地址
            self.brokers_address[id] = row.contents[5].text.strip().replace('\n', '')
            # 存入到持股数量表
            n = int(row.contents[7].text.strip().replace(',', ''))
            self.brokers_postion[id] = n

    def get_brokerPostion(self, name):
        idx = self.brokers_name.index(name)
        return self.brokers_postion[self.brokers_id[idx]]



#***********************************************************************************************************************
"""
unittest
"""
searchHtmlCatchPath = './data/HKEXSearchCach'

class TestHKEXBrokersPage(unittest.TestCase):

    def setUp(self):
        self.path = searchHtmlCatchPath + '/20180710.html'
        self.page = HKEXBrokersPage(self.path)

    # 检查是否持股日期和文件名字一致
    def test_loadpage(self):
        dtFile = datetime.datetime.strptime(self.path[-13:-5], '%Y%m%d')  # 文件名中的日期
        self.assertEqual(self.page.postion_date, dtFile)
        self.assertEqual(self.page.stock_code, '00700')

    # 检查列表是否加载完成
    def test_listdata(self):
        self.assertEqual(self.page.get_brokerPostion('高盛(亚洲)证券有限公司'), 374695248)
        self.assertEqual(self.page.brokers_postion['C00019'], 1586739828)
        self.assertEqual(self.page.brokers_address['C00019'], 'HSBC WEALTH BUSINESS SERVICES 8/F TOWER 2 & 3 HSBC CENTRE 1 SHAM MONG ROAD KOWLOON')
        self.assertEqual(self.page.brokers_postion['B02106'], 100)
        self.assertEqual(self.page.brokers_address['B02106'], 'RM 2401-2402 24/F JUBILEE CENTRE 46 GLOUCESTER ROAD WANCHAI HONG KONG')

    def test_brokersId2Name(self):
        idx=self.page.brokers_name.index('高盛(亚洲)证券有限公司')
        self.assertEqual(self.page.brokers_id[idx], 'B01451')

        idx=self.page.brokers_name.index('香港上海汇丰银行有限公司')
        self.assertEqual(self.page.brokers_id[idx], 'C00019')

        idx=self.page.brokers_name.index('JPMORGAN CHASE BANK, NATIONAL ASSOCIATION')
        self.assertEqual(self.page.brokers_id[idx], 'C00100')

if __name__ == '__main__':
    unittest.main()
