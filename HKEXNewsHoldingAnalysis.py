#-*- coding: utf-8 -*-
"""
#读取大行持仓
#根据各个大行持有仓位信息进行分析
#数据来源http://sc.hkexnews.hk/TuniS/www.hkexnews.hk/sdw/search/searchsdw_c.aspxh
"""
import os

import datetime
import numpy as np
import pandas as pd

from selenium import webdriver
from selenium.webdriver.support.ui import Select

import bs4
import re



HKEXNewsSearchPath = 'http://sc.hkexnews.hk/TuniS/www.hkexnews.hk/sdw/search/searchsdw_c.aspx'
searchHtmlCatchPath = './data/HKEXSearchCach'

#填写表单，搜索结果
def GetHKEXNewsSearchPage(driver, stockcode, date = datetime.date.today() - datetime.timedelta(days=1)):
    print('GetHKEXNewsHoldingData(%s,%s) begin\n'%(stockcode, date))
    print('searchpath = %s\n'%HKEXNewsSearchPath)
    driver.get(HKEXNewsSearchPath)
    # 填写年月日
    deltadays = datetime.date.today() - date
    assert deltadays.days > 365 or deltadays.days < 0, 'error ！！！ 只能支持一年内的数据\n'

    dayidx = date.day - 1
    monthidx = date.month - 1
    yearidx = datetime.date.today().year - date.year


    ddlShareholdingDay = Select(driver.find_element_by_name('ddlShareholdingDay'))
    ddlShareholdingMonth = Select(driver.find_element_by_name('ddlShareholdingMonth'))
    ddlShareholdingYear = Select(driver.find_element_by_name('ddlShareholdingYear'))

    ddlShareholdingYear.select_by_index(yearidx)
    ddlShareholdingMonth.select_by_index(monthidx)
    ddlShareholdingDay.select_by_index(dayidx)
    # 填写股票代码
    txtStockCode = driver.find_element_by_name('txtStockCode')
    txtStockCode.send_keys(stockcode)
    search_box = driver.find_element_by_name('btnSearch')
    search_box.click()
    print(driver.page_source)
    print('GetHKEXNewsHoldingData() end\n')

    return driver.page_source


#下载昨天的页面
def SaveYesterday2Html():
    stockcode = '00700'
    yesterday = datetime.date.today() - datetime.timedelta(days=1)
    htmlPage = GetHKEXNewsSearchPage(driver, stockcode, yesterday)
    if not os.path.exists(searchHtmlCatchPath):
        os.mkdir(searchHtmlCatchPath)
    filename = searchHtmlCatchPath + '/' + yesterday.strftime('%Y%m%d') + '.html'
    fo = open(filename, 'w+')
    fo.write(htmlPage)
    fo.close()

#下载昨天到过去365天的数据
def DownloadHKEXNewsPages365(driver, stockcode):
    for idx in range(365):
        date = datetime.date.today() - datetime.timedelta(days=1 + idx)
        filename = searchHtmlCatchPath + '/' + date.strftime('%Y%m%d') + '.html'
        if not os.path.exists(filename):
            htmlPage = GetHKEXNewsSearchPage(driver, stockcode, date)
            fo = open(filename, 'w+')
            fo.write(htmlPage)
            fo.close()

#处理HKEXNewsPages，导出数据到pandas.dataframe对象
def PageData2DataFrame():
    pageFilePath = searchHtmlCatchPath + '/20180710.html'

    pageFile = open(pageFilePath)
    soup = bs4.BeautifulSoup(pageFile, "lxml")

    tableParent = soup.select_one('#participantShareholdingList')
    #print(tableParent.tbody)

    table = tableParent.find_all('tr', re.compile("^row"))
    print(table)

    pageFile.close()


if __name__ == "__main__" :

    print('HKEXNewsHoldingAnalysis.py')

    chromeopt = webdriver.ChromeOptions()
    chromeopt.add_argument('-headless')
    driver = webdriver.Chrome(chrome_options=chromeopt)  # Optional argument, if not specified will search path.
    #driver = webdriver.PhantomJS()

    stockcode = '00700'
    #SaveYesterday2Html()

    DownloadHKEXNewsPages365(driver, stockcode)

    PageData2DataFrame()

    driver.quit()