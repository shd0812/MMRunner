import unittest
from mlib.m_expection import *
import HTMLTestRunner
import time
from mlib.logger import myLog
import os

logger =myLog.getLog()

class Test_Suit(object):


    # 通过路径寻找所有用例
    @staticmethod
    def creatsuite(case_path):
        if not case_path:
            case_path = r'D:\Python\flask_mock\API_Unitest\tests_cases'
        testunit = unittest.TestSuite()
        discover = unittest.defaultTestLoader.discover(case_path, pattern='test_http.py', top_level_dir=None)
        for test_suit in discover:
            for test_case in test_suit:
                testunit.addTests(test_case)

        return testunit
    @staticmethod
    def run(case_path):


        alltestnames = Test_Suit.creatsuite(case_path)
        now = time.strftime("%Y-%m-%M-%H_%M_%S", time.localtime(time.time()))
        #reports_dir_path = "..\\reports\\"  #'D:\Python\flask_mock\reports'
        reports_dir_path = "reports\\"  #  D:\Python\flask_mock\API_Unitest\reports
        if not os.path.isdir(reports_dir_path):
            os.mkdir(reports_dir_path)
        filename =reports_dir_path + now +'result.html'  # 定义个报告存放路径，支持相对路径。
        with open(filename, 'wb') as f:
            runner = HTMLTestRunner.HTMLTestRunner(stream=f, title='111111', description ='2222')
            runner.run(alltestnames)


if __name__ == '__main__':
    Test_Suit.run(r'D:\MMRunner\temp_test')