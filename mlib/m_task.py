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

        for item in api_list:
            method = extract_str_from_filed('request.method', item)
            url = extract_str_from_filed('request.url', item)
            data_dic = extract_str_from_filed('request.data', item)
            dic = tmpFunc(data_dic)
            rel = self.api_client.request(method, url, data=dic)
            reslut = json.loads(rel.text)
            # print(reslut)
            self.assertEqual(reslut.get('totalCount'), 12)



def factory(apidata):
    def tool(self):
        Test_Case.product_case(self,apidata)
    setattr(tool, '__doc__', u'测试%s' % str(apidata[0]))
    print(tool.__doc__)
    return tool
def testall(apidata):
    for i in range(len(apidata)):
     setattr(Test_Case,'test_'+str(i+1),factory(apidata[i]))