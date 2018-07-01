"""
根据腾讯公告提取财报日期
https://www.tencent.com/zh-cn/notice_timeline.html
"""

from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
from datetime import datetime
import re

xlsPath = './data/700ReportsDate.xls'
htmPath = './data/700公告页面.htm'


def GetReportsDates2Excel():
    soup = BeautifulSoup(open(htmPath), "lxml")
    datelist = []
    textlist = []
    for tag in soup.find_all(text=re.compile("业绩公布")):
        previous_date = tag.find_previous("span", attrs={"class": "date"})
        print(previous_date.text)
        datelist.append(datetime.strptime(previous_date.text, '%Y/%m/%d'))

        print(tag)
        textlist.append(tag)
    reportDates = pd.DataFrame({'Date': datelist,
                                'Reports': textlist})
    reportDates.to_excel(xlsPath, sheet_name='700Reports')


if __name__ == "__main__" :
    print('FinacialReportDate.py main')

    GetReportsDates2Excel()


    print('FinacialReportDate.py main end')