import unittest
import os,json,time
import HTMLTestRunner
from mlib.m_client import HttpSession
from mlib.utils import  *
from  XennHo.utils import input_parm

def tmpFunc(p_dic):
    for var_k, var_v in p_dic.items():
        result = var_k + '=' + var_v
        result = input_parm(result)
        #print(result)
        return result


class Test_Case(unittest.TestCase):
    def setUp(self):
        self.api_client = HttpSession('https://mi.shaxiaoseng.com:4433/Xeenho/')


    def product_case(self,api_list):

        method = extract_str_from_filed('request.method', api_list)
        url = extract_str_from_filed('request.url', api_list)
        data_dic = extract_str_from_filed('request.data', api_list)
        dic = tmpFunc(data_dic)
        rel = self.api_client.request(method, url, data=dic)
        reslut = json.loads(rel.text)
            # print(reslut)
        self.assertEqual(reslut.get('totalCount'), 12)



def factory(apidata):
    print(22234234234234)
    print(apidata)
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
            }

    },
        {
            'name': '查询用户投资记录',
            'request': {
                'method': 'POST',
                'url': 'query_userbidrepayinfo',
                'data': {
                    'platform_uid': '3000000419294000'
                }
            }

        }
    ]
    print(apidata)
    run(apidata)