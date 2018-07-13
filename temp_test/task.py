import unittest
import time
import HTMLTestRunner
from test_case.case_one import run_single_testcase
from mlib.utils import  *





class Test_Case(unittest.TestCase):
    def setUp(self):
        pass

    def product_case(self,apidata):
        back = run_single_testcase(apidata)
        for item in back:
            s = do_validation(item[0], item[1], item[2])
            self.assertTrue(s,'实际为{},期望为{}'.format(item[1],item[2]))





def factory(apidata):
    def tool(self):
        Test_Case.product_case(self,apidata)
    setattr(tool, '__doc__', u'测试%s' % str(apidata['name']))

    return tool

def testall(apidata):
    nameList = []
    for i in range(len(apidata)):
        name = 'test_' + str(i + 1)
        setattr(Test_Case, name, factory(apidata[i]))
        nameList.append(name)
    return nameList

def suite(apidata):

    nameList = testall(apidata)
    print(nameList)
    suites =unittest.TestSuite()
    for i in nameList:
        suites.addTest(Test_Case(i))
    return suites
def run(apidata):
    now = time.strftime("%Y-%m-%M-%H_%M_%S", time.localtime(time.time()))
    reports_dir_path = "reports\\"  # D:\Python\flask_mock\API_Unitest\reports
    if not os.path.isdir(reports_dir_path):
        os.mkdir(reports_dir_path)
    filename = reports_dir_path + now + 'result.html'  # 定义个报告存放路径，支持相对路径。
    with open(filename, 'wb') as f:
        runner = HTMLTestRunner.HTMLTestRunner(stream=f, title='111111', description='2222')
        runner.run(suite(apidata))

if __name__ == "__main__":
    #apidata = ['登录','退出']  #设置接口函数名
    apidata = [{
            'name':'查询用户资金',
            'request':{
                'method': 'POST',
                'url': 'query_useraccount',
                'data':{
                    'platform_uid':'3000000419294000'
                }
            },
            'validate':[
                {'eq':['records.0.platform_uid', '30000004191860002']},
                {'eq': ['records.0.assetsAmount', '1000.001']}

            ]

    },
        {
            'name': '查询用户投资记录',
            'request': {
                'method': 'POST',
                'url': 'query_userbidrepayinfo',
                'data': {
                    'platform_uid': '3000000419294000'
                }
            },
            'validate':[
                {'eq':['records.0.bidRecords.0.productBidId', 'XY1806046325972406']},
                {'eq': ['totalCount', 6]}

            ]

        }
    ]
    print(apidata)
    run(apidata)