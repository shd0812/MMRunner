import unittest
import os,json,time
import HTMLTestRunner
from mlib.utils import  *
from mconf.setting import REPORT_PATH,REPORT_TITLE,REPORT_DESCRIPTION
#from test_case.case_one import run_single_testcase
from test_case.sxs_case_api import run_single_testcase


class Test_Case(unittest.TestCase):
    def setUp(self):
        pass

    def product_case(self,apidata):
        back = run_single_testcase(apidata)
        for item in back:
            s = do_validation(item[0], item[1], item[2])
            self.assertTrue(s,'实际为{},期望为{}'.format(item[1],item[2]))


#批量创建 test函数
def factory(apidata):

    def tool(self):
        Test_Case.product_case(self,apidata)
    setattr(tool, '__doc__', u'测试%s' % str(apidata['name']))
    return tool

#生成test_case 的名字
def testall(apidata):
    nameList = []
    for i in range(len(apidata)):
        name = 'test_' + str(i + 1)
        setattr(Test_Case, name, factory(apidata[i]))
        nameList.append(name)
    return nameList

#把所有的case加入suit里
def suite(apidata):
    nameList = testall(apidata)
   # print(nameList)
    suites =unittest.TestSuite()
    for i in nameList:
        suites.addTest(Test_Case(i))
    return suites
#开始运行测试用例
def run(apidata):
    now = time.strftime("%Y-%m-%M-%H_%M_%S", time.localtime(time.time()))
    if not os.path.isdir(REPORT_PATH):
        os.mkdir(REPORT_PATH)
    filename =  now + 'result.html' # 定义个报告存放路径，支持相对路径。
    file_path = os.path.join(REPORT_PATH,filename)
    with open(file_path, 'wb') as f:
        runner = HTMLTestRunner.HTMLTestRunner(stream=f, title=REPORT_TITLE, description=REPORT_DESCRIPTION)
        runner.run(suite(apidata))

