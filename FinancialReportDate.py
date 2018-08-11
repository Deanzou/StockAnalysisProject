# -*- coding: utf-8 -*-
"""
根据腾讯公告提取财报日期
https://www.tencent.com/zh-cn/notice_timeline.html
"""

from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
from datetime import datetime
import re

import unittest

csvPath = u'/700ReportsDate.csv'
htmPath = u'/700公告页面.htm'

class ReportsDate:
    def __init__(self, home):
        self.home = home
        self.dfdates = pd.DataFrame()

    def saveReportsDate2csv(self):
        soup = BeautifulSoup(open(self.home+htmPath), "lxml")
        datelist = []
        textlist = []
        for tag in soup.find_all(text=re.compile(u"业绩公布")):
            previous_date = tag.find_previous("span", attrs={"class": "date"})
            print(previous_date.text)
            datelist.append(datetime.strptime(previous_date.text, '%Y/%m/%d'))

            print(tag)
            textlist.append(tag)

        self.dfdates = pd.DataFrame(textlist, columns=['Reports'], index=datelist)
        self.dfdates.to_csv(self.home + csvPath)

    def getReportsDate(self):
        print('getReportsDate begin')
        self.dfdates = pd.read_csv(self.home + csvPath, index_col=0, parse_dates=True)
        print(self.dfdates)
        print('getReportsDate end')
        return self.dfdates

"""
unittest
"""
class TestReportsDate(unittest.TestCase):
    def setUp(self):
        self.repotsdate = ReportsDate(home='./data/HKEXSearchCach00700')

    def test_getReportsDate2Exl(self):
        self.repotsdate.saveReportsDate2csv()
        self.repotsdate.getReportsDate()


if __name__ == "__main__":
    unittest.main()

