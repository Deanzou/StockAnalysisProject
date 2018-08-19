# -*- coding: utf-8 -*-
"""
管理所有的文件，并汇总到DataFrame
#数据来源http://sc.hkexnews.hk/TuniS/www.hkexnews.hk/sdw/search/searchsdw_c.aspxh
"""
import os

import datetime
import pandas as pd

from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import WebDriverException

import bs4
import re


from HKEXBrokersPage import HKEXBrokersPage


import unittest

HKEXNewsSearchPath = 'http://sc.hkexnews.hk/TuniS/www.hkexnews.hk/sdw/search/searchsdw_c.aspx'


class HKEXBrokersPosDatabase(object):

    def __init__(self, path, code):
        self.path = path
        self.df_id2names = pd.DataFrame()
        self.df_brokersPos = pd.DataFrame()
        self.code = code
        self.driver = None

    def __del__(self):
        if self.driver is not None:
            self.driver.quit()

    def init_webdriver(self):
        chromeopt = webdriver.ChromeOptions()
        chromeopt.add_argument('-headless')
        self.driver = webdriver.Chrome(options=chromeopt)  # Optional argument, if not specified will search path.
        #driver = webdriver.PhantomJS()

    # 填写表单，搜索结果
    def getHKEXNewsSearchPage(self, stockcode, date=datetime.date.today() - datetime.timedelta(days=1)):
        print('HKEXBrokersPosDatabase.getHKEXNewsHoldingData(%s,%s) begin\n' % (stockcode, date))
        print('searchpath = %s\n' % HKEXNewsSearchPath)
        self.driver.get(HKEXNewsSearchPath)

        assert "No results found." not in self.driver.page_source

        # 填写年月日
        deltadays = datetime.date.today() - date
        assert deltadays.days <= 365 and deltadays.days > 0, 'error ！！！ 只能支持一年内的数据\n'

        dayidx = date.day - 1
        monthidx = date.month - 1
        yearidx = datetime.date.today().year - date.year

        ddlShareholdingDay = Select(self.driver.find_element_by_name('ddlShareholdingDay'))
        ddlShareholdingMonth = Select(self.driver.find_element_by_name('ddlShareholdingMonth'))
        ddlShareholdingYear = Select(self.driver.find_element_by_name('ddlShareholdingYear'))

        ddlShareholdingYear.select_by_index(yearidx)
        ddlShareholdingMonth.select_by_index(monthidx)
        ddlShareholdingDay.select_by_index(dayidx)
        # 填写股票代码
        txtStockCode = self.driver.find_element_by_name('txtStockCode')
        txtStockCode.send_keys(stockcode)
        search_box = self.driver.find_element_by_name('btnSearch')
        search_box.click()
        # print(driver.page_source)
        print('HKEXBrokersPosDatabase.getHKEXNewsHoldingData() end\n')

        element_list = self.driver.find_element_by_id("participantShareholdingList")

        return self.driver.page_source

    def GetPageDate(self, page):
        soup = bs4.BeautifulSoup(page, "lxml")
        holdDateTitle = soup.find(text=re.compile("持股日期:"))
        holdDate = holdDateTitle.parent.find_next('td', attrs={"class": "arial12black", "nowrap": "nowrap"})
        if holdDate != None:
            holdDateText = holdDate.text.strip()  # 页面日期格式%D/%M/%Y
            return datetime.datetime.strptime(holdDateText, '%d/%m/%Y')

    # 下载昨天到过去365天的数据
    # 网站只支持下载一年数据

    def downloadHKEXNewsPages365(self):
        print("HKEXBrokersPosDatabase.downloadHKEXNewsPage365 begin")
        for idx in range(365):
            date = datetime.date.today() - datetime.timedelta(days=1 + idx)
            filename = self.path + '/' + date.strftime('%Y%m%d') + '.html'
            if not os.path.exists(filename):
                try:
                    htmlPage = self.getHKEXNewsSearchPage(self.code, date)
                    eleDate = self.driver.find_element_by_xpath(
                        "//div[@id='pnlResultHeader']/table/tbody/tr[2]/td/table/tbody/tr/td[2]")
                    pageDate = datetime.datetime.strptime(eleDate.text, "%d/%m/%Y")
                    # filename = searchHtmlCatchPath + '/' + pageDate.strftime('%Y%m%d') + '.html'
                    if pageDate.date() != date:
                        print("HKEXBrokersPosDatabase. download warnning!!! pagedate != date %s" % filename)

                except WebDriverException as e:
                    print("HKEXBrokersPosDatabase. download %s error!!", filename)
                    print(e)
                else:
                    fo = open(filename, 'w+')
                    assert fo
                    fo.write(htmlPage)
                    fo.close()
                    print('HKEXBrokersPosDatabase. download %s success!!' % filename)

        print("HKEXBrokersPosDatabase.downloadHKEXNewsPage365 end")

    def process_allpages(self):
        for root, dirs, files in os.walk(self.path):
            for filepath in files:
                pagepath = os.path.join(self.path, filepath)
                if pagepath[-5:] == '.html':
                    print("HKEXBrokersPosDatabase::process_allpages HKEXBrokersPage(%s)"%pagepath)
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
                        self.save_csv('HKEXBrokersPosDatabase::process_allpages brokers_position_tmp_%s.csv'%filepath)

    def save_csv(self, filename =''):
        print('HKEXBrokersPosDatabase::save_csv begin')
        if self.code is None:
            self.code = 'nonecode'
            print("HKEXBrokersPosDatabase::process error stock code == None!!!!")

        if filename == '':
            filename = self.path + '/brokers_postion_%s.csv'%self.code
        else:
            filename = self.path + '/' + filename
        print(self.df_brokersPos)
        self.df_brokersPos.to_csv(filename)
        print('HKEXBrokersPosDatabase::save_csv end')

    def load_csv(self,filename=''):
        print('HKEXBrokersPosDatabase::load_csv begin')
        if self.code is None:
            self.code = 'nonecode'
            print("HKEXBrokersPosDatabase::process error stock code == None!!!!")

        if filename == '':
            filename = self.path + '/brokers_postion_%s.csv'%self.code
        else:
            filename = self.path + '/' + filename

        fdpos = pd.read_csv(filename, index_col=0, parse_dates=True)
        self.df_brokersPos = pd.concat([self.df_brokersPos, fdpos])

    def get_latestday(self):
        return self.df_brokersPos.index[-1].date()

    # 港交所坑爹，仓位数据是延迟两天的
    def get_realdatedata(self):
        return self.df_brokersPos.shift(-2)
# ***********************************************************************************************************************
"""
unittest
"""


class TestHKEXBrokersPosDatabase(unittest.TestCase):
    def setUp(self):
        print("TestHKEXBrokersPosDatabase::setUp begin")
        self.searchHtmlCatchPath = './data/HKEXSearchCach00700'
        self.database = HKEXBrokersPosDatabase(self.searchHtmlCatchPath, '00700')

    def test_download365data(self):
        self.database.init_webdriver()
        self.database.downloadHKEXNewsPages365()

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
