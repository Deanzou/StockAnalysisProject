"""
#读取大行持仓
#根据各个大行持有仓位信息进行分析
#数据来源http://sc.hkexnews.hk/TuniS/www.hkexnews.hk/sdw/search/searchsdw_c.aspxh
"""

import time
import  pandas as pd
from selenium import webdriver
from selenium.webdriver.support.ui import Select


HKEXNewsSearchPath = 'http://sc.hkexnews.hk/TuniS/www.hkexnews.hk/sdw/search/searchsdw_c.aspx'

if __name__ == "__main__" :

    print('HKEXNewsHoldingAnalysis.py')

    #driver = webdriver.Chrome()  # Optional argument, if not specified will search path.
    driver = webdriver.PhantomJS()
    driver.get(HKEXNewsSearchPath)

    #填写年月日
    ddlShareholdingDay = Select(driver.find_element_by_name('ddlShareholdingDay'))
    ddlShareholdingMonth = Select(driver.find_element_by_name('ddlShareholdingMonth'))
    ddlShareholdingYear = Select(driver.find_element_by_name('ddlShareholdingYear'))

    ddlShareholdingYear.select_by_index(0)
    ddlShareholdingMonth.select_by_index(5)
    ddlShareholdingDay.select_by_index(28)

    #填写股票代码
    txtStockCode = driver.find_element_by_name('txtStockCode')
    txtStockCode.send_keys('00700')

    search_box = driver.find_element_by_name('btnSearch')
    search_box.click()

    print(driver.page_source)


    driver.quit()