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
from selenium.common.exceptions import WebDriverException

import bs4
import re

from HKEXBrokersPage import HKEXBrokersPage
from HKEXNewsDatabase import HKEXNewsDatabase



HKEXNewsSearchPath = 'http://sc.hkexnews.hk/TuniS/www.hkexnews.hk/sdw/search/searchsdw_c.aspx'
searchHtmlCatchPath = './data/HKEXSearchCach00700'

#填写表单，搜索结果
def GetHKEXNewsSearchPage(driver, stockcode, date = datetime.date.today() - datetime.timedelta(days=1)):
    print('GetHKEXNewsHoldingData(%s,%s) begin\n'%(stockcode, date))
    print('searchpath = %s\n'%HKEXNewsSearchPath)
    driver.get(HKEXNewsSearchPath)

    assert "No results found." not in driver.page_source

    # 填写年月日
    deltadays = datetime.date.today() - date
    assert deltadays.days <= 365 and deltadays.days > 0, 'error ！！！ 只能支持一年内的数据\n'

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
    #print(driver.page_source)
    print('GetHKEXNewsHoldingData() end\n')

    element_list = driver.find_element_by_id("participantShareholdingList")

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

def GetPageDate(page):
    soup = bs4.BeautifulSoup(page, "lxml")
    holdDateTitle = soup.find(text=re.compile("持股日期:"))
    holdDate = holdDateTitle.parent.find_next('td', attrs={"class": "arial12black", "nowrap": "nowrap"})
    if holdDate != None:
        holdDateText = holdDate.text.strip()  # 页面日期格式%D/%M/%Y
        return datetime.datetime.strptime(holdDateText, '%d/%m/%Y')

#下载昨天到过去365天的数据
#网站只支持下载一年数据
def DownloadHKEXNewsPages365(driver, stockcode):
    print("DownloadHKEXNewsPage365 begin")
    for idx in range(365):
        date = datetime.date.today() - datetime.timedelta(days=1 + idx)
        filename = searchHtmlCatchPath + '/' + date.strftime('%Y%m%d') + '.html'
        if not os.path.exists(filename):
            try:
                htmlPage = GetHKEXNewsSearchPage(driver, stockcode, date)
                eleDate = driver.find_element_by_xpath("//div[@id='pnlResultHeader']/table/tbody/tr[2]/td/table/tbody/tr/td[2]")
                pageDate = datetime.datetime.strptime(eleDate.text, "%d/%m/%Y")
                #filename = searchHtmlCatchPath + '/' + pageDate.strftime('%Y%m%d') + '.html'
                if pageDate.date() != date:
                    print("download warnning!!! pagedate != date %s"%filename)

            except WebDriverException as e:
                print("download %s error!!", filename)
                print(e)
            else:
                fo = open(filename, 'w+')
                assert fo
                fo.write(htmlPage)
                fo.close()
                print('download %s success!!'%filename)

    print("DownloadHKEXNewsPage365 end")


#处理HKEXNewsPages，导出数据到pandas.dataframe对象
def PageData2DataFrame(pageFilePath):
    print("PageData2DataFrame begin")

    page = HKEXBrokersPage(pageFilePath)


    return page.get_brokersPostionDataFrame(), page.get_brokersId2NameDataFrame()

    print("PageData2DataFrame end")


if __name__ == "__main__" :

    print('HKEXNewsHoldingAnalysis.py main begin')

    chromeopt = webdriver.ChromeOptions()
    chromeopt.add_argument('-headless')
    try :
        driver = webdriver.Chrome(chrome_options=chromeopt)  # Optional argument, if not specified will search path.
        #driver = webdriver.PhantomJS()

        stockcode = '00700'
        DownloadHKEXNewsPages365(driver, stockcode)

    except Exception as e:
        print("DownloadHKEXNewsPages365 error!!!")
        print(e)

    finally:
        driver.quit()
        print('HKEXNewsHoldingAnalysis.py main end')

    print("HKEXNewsDatabase begin")
    database = HKEXNewsDatabase(searchHtmlCatchPath, '00700')

    try:
        database.load_csv()
        database.process_allpages()
        database.save_csv()
    except Exception as e:
        print(e)
        pass

    print("HKEXNewsDatabase end")
