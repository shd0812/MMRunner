import unittest
import os,json,time
import HTMLTestRunner
from mlib.m_client import HttpSession
from mlib.utils import  *
from mconf.setting import REPORT_PATH,REPORT_TITLE,REPORT_DESCRIPTION
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
        expect_dic = extract_str_from_filed('expect', api_list)
        logger.m_error(str(expect_dic))
        dic = tmpFunc(data_dic)
        rel = self.api_client.request(method, url, data=dic)
        reslut = json.loads(rel.text)
        #self.assertEqual(reslut.get('totalCount'), 12)
        for k,v in expect_dic.items():
            var_k = extract_str_from_filed(k, reslut)
            print(k)
            self.assertEqual(var_k,v,'实际值为{},期待值为{}'.format(var_k,v))


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
            'expect':{
                'records.0.assetsAmount': '1000.001'
            }

    },
        {
            'name': '啊啊查询用户投资记录',
            'request': {
                'method': 'POST',
                'url': 'query_userbidrepayinfo',
                'data': {
                    'platform_uid': '3000000419294000'
                }
            },
            'expect': {
                'records.0.bidRecords.0.productBidId': 'XY1806046325972406'
            }

        }
    ]
    run(apidata)