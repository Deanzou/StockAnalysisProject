#-*- coding: utf-8 -*-
"""
#读取大行持仓
#根据各个大行持有仓位信息进行分析
#数据来源http://sc.hkexnews.hk/TuniS/www.hkexnews.hk/sdw/search/searchsdw_c.aspxh
#绘制图表
"""
import unittest
import os
import datetime
import numpy as np
import pandas as pd
import math

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontManager, FontProperties

import seaborn as sns


from HKEXBrokersPosDatabase import HKEXBrokersPosDatabase
from StockHisData import StockHisData

searchHtmlCatchPath = './data/HKEXSearchCach00700'


def getChineseFont():
    return FontProperties(fname='/System/Library/Fonts/PingFang.ttc')


class BrokersAnalysis(object):

    def __init__(self):
        self.brokerspos = HKEXBrokersPosDatabase(searchHtmlCatchPath, '00700')
        self.stockhisdata = StockHisData(searchHtmlCatchPath, "0700.HK")
        self.reportsdates = pd.read_csv(searchHtmlCatchPath + '/700ReportsDate.csv', index_col=0, parse_dates=True)

        #初始化字体和风格
        sns.set(style="darkgrid")
        matplotlib.rcParams['font.sans-serif'] = 'WenQuanYi Micro Hei'
        return

    def process_data_daily(self):
        try:
            self.brokerspos.init_webdriver()
            self.brokerspos.downloadHKEXNewsPages365()

            self.brokerspos.load_csv()
            self.brokerspos.process_allpages()
            self.brokerspos.save_csv()

            self.stockhisdata.update_csv()
        except Exception as e:
            print(e)
            pass

    def load_data(self):
        self.brokerspos.load_csv()
        self.stockhisdata.load_csv()

    def draw_grid(self):
        #需要分析的券商
        dicBrokers = {'B01451': u"高盛",
                      'B01274': u"MORGAN STANLEY",
                      'B01161': u"UBS HK",
                      'C00100': u"JPMORGAN",
                      'B01121': u"法兴 HK",
                      'A00003': u"中国证券登记结算有限责任公司",
                      'C00019': u"汇丰",
                      'C00039': u"渣打",
                      'B01130': u"中银国际",
                      'B01955': u"富途",
                      }
        #持续时长
        timeperiod = 300
        result = pd.DataFrame()
        result = self.stockhisdata.stockprice.join(self.brokerspos.df_brokersPos)
        reportdates = self.reportsdates[(self.reportsdates.index >= result.index[-timeperiod]) &
                                        (self.reportsdates.index <= result.index[-1])]

        fig, axs = plt.subplots(math.ceil(len(dicBrokers) / 2), ncols=2, figsize=(15, 12), sharex=True)
        fig.suptitle(u"大行持仓", fontproperties=getChineseFont())
        row = 0
        col = 0
        idx = 0
        lc = None#用于图例
        ld = None
        for key, name in dicBrokers.items():
            closedatas = result['Close'].iloc[-timeperiod:]
            lc = axs[row][col].plot(closedatas, c='r')
            # axs[row][col].grid(False)
            axs[row][col].set_title(name)
            ax2 = axs[row][col].twinx()
            ax2.plot(result[key].iloc[-timeperiod:], c='b')
            #ax2.legend(loc='upper right')
            # 画财报日期提示线条
            for day in reportdates.index:
                ld = axs[row][col].fill_between([day],
                                                closedatas.min()-5,
                                                closedatas.max()+5,
                                                color='g', linestyle=':', lw=1.5)
                axs[row][col].annotate(day.strftime("%m-%d"),
                                       xy=(day.date(), closedatas.min()-5))

            idx += 1
            col = idx % 2
            row = idx // 2

        fig.legend(lc, (self.stockhisdata.code,), 'upper left')
        fig.legend((ld,), (u'财报日',), 'upper right')
        plt.show()

# ***********************************************************************************************************************
"""
unittest
"""


class TestBrokersAnalysis(unittest.TestCase):
    def setUp(self):
        self.analyzer = BrokersAnalysis()

    def test_processdata_daily(self):
        #self.analyzer.process_data_daily()
        self.analyzer.load_data()
        self.analyzer.draw_grid()


if __name__ == '__main__':
    unittest.main()