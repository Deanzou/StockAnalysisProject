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



HKEXNewsSearchPath = 'http://sc.hkexnews.hk/TuniS/www.hkexnews.hk/sdw/search/searchsdw_c.aspx'
searchHtmlCatchPath = './data/HKEXSearchCach'

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
#网站只支持下载一年数据
def DownloadHKEXNewsPages365(driver, stockcode):
    print("DownloadHKEXNewsPage365 begin")
    for idx in range(365):
        date = datetime.date.today() - datetime.timedelta(days=1 + idx)
        filename = searchHtmlCatchPath + '/' + date.strftime('%Y%m%d') + '.html'
        if not os.path.exists(filename):
            try:
                htmlPage = GetHKEXNewsSearchPage(driver, stockcode, date)
            except WebDriverException as e:
                print("download %s error!!", filename)
                print(e)
            else:
                fo = open(filename, 'w+')
                assert fo
                fo.write(htmlPage)
                fo.close()
    print("DownloadHKEXNewsPage365 end")


#处理HKEXNewsPages，导出数据到pandas.dataframe对象
def PageData2DataFrame(pageFilePath):
    print("PageData2DataFrame begin")
    soup = None
    try:
        pageFile = open(pageFilePath)
        assert pageFile
        soup = bs4.BeautifulSoup(pageFile, "lxml")
    finally:
        pageFile.close()

    #检查是否持股日期和文件名字一致
    holdDateTitle = soup.find(text=re.compile("持股日期:"))
    holdDate = holdDateTitle.parent.find_next('td', attrs={"class": "arial12black", "nowrap": "nowrap"})
    holdDateText = holdDate.text.strip() #页面日期格式%D/%M/%Y
    dtholdDate = datetime.datetime.strptime(holdDateText, '%d/%m/%Y')
    dtFile = datetime.datetime.strptime(pageFilePath[-13:-5], '%Y%m%d')#文件名中的日期
    assert dtFile == dtholdDate
    if dtholdDate != dtFile :
        print("PageData2DataFrame(%s) error end!! holding time != filenametime ", pageFilePath)
        return

    tableParent = soup.select_one('#participantShareholdingList')
    #print(tableParent.tbody)

    table = tableParent.find_all('tr', re.compile("^row"))
    #print(table)
    tableDic = {}#页面对应字典 参与者编号 ： 持股数量
    ids = []#参与者编号
    names = []#参与者名称
    for row in table:
        # print(row.contents[1].text)#参与者编号
        # print(row.contents[3].text)#中央结算系统参与者名称(*即愿意披露的投资者户口持有人)
        # print(row.contents[5].text)#地址
        # print(row.contents[7].text)#持股数量
        # print(row.contents[9].text)#占已发行股份/权证/单位百分比
        #存入到名字id映射表中
        id = row.contents[1].text.strip().replace('\n', '')
        name = row.contents[3].text.strip().replace('\n', '')
        if id == '':
            id = name
        assert not id in ids, '页面中参与者编号和名称不应该重复'
        ids.append(id)
        names.append(name)
        #存入到持股数量表
        n = int(table[0].contents[7].text.strip().replace(',',''))
        tableDic[id] = n

    print(tableDic)
    # print(ids)
    # print(names)

    dtidx = pd.DatetimeIndex([dtholdDate])
    df = pd.DataFrame(tableDic, dtidx)
    return df, pd.DataFrame(names, index=ids)

    print("PageData2DataFrame end")


if __name__ == "__main__" :

    print('HKEXNewsHoldingAnalysis.py')

    chromeopt = webdriver.ChromeOptions()
    chromeopt.add_argument('-headless')
    try :
        driver = webdriver.Chrome(chrome_options=chromeopt)  # Optional argument, if not specified will search path.
        #driver = webdriver.PhantomJS()
    finally:
        driver.quit()

    stockcode = '00700'
    #SaveYesterday2Html()

    try:
        DownloadHKEXNewsPages365(driver, stockcode)
    except Exception:
        print("DownloadHKEXNewsPages365 error!!!")
        pass

    dfBrokerId2Name = pd.DataFrame()
    dfBrokersPostion = pd.DataFrame()
    pageFilePath = searchHtmlCatchPath + '/20180710.html'
    dfBrokersPostion, dfBrokerId2Name = PageData2DataFrame(pageFilePath)

    print(dfBrokerId2Name)
    print(dfBrokersPostion)