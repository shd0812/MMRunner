from mlib.mclient import HttpSession

from  XennHo.utils import input_parm
from mlib.loadcase import TestLoad
from mlib.utils import  *
import unittest,json


# host = 'https://mi.shaxiaoseng.com:4433/Xeenho/'
# api_client = HttpSession(host)
#
# parm_str = 'platform_uid=3000000419294000_m'
# dic = input_parm(parm_str)
# res=api_client.request('POST','query_useraccount',data=dic)
# print(res.text)
def tmpFunc(p_dic):
    for var_k, var_v in p_dic.items():
        result = var_k + '=' + var_v
        result = input_parm(result)
        #print(result)
        return result


class TestApi(unittest.TestCase):
    def setUp(self):
        result = TestLoad.load_file('../data/test_one/demo_api.yaml')
        config_dic = result[0]
        self.test_list = result[1]
        self.api_client = HttpSession(extract_str_from_filed('base_url', config_dic))


    def tearDown(self):
        pass
        "do something after test.Clean up."

    def test_one(self):
        test_one = self.test_list[0]
        method = extract_str_from_filed('request.method', test_one)
        url = extract_str_from_filed('request.url', test_one)
        data_dic = extract_str_from_filed('request.data', test_one)
        dic = tmpFunc(data_dic)
        rel =self.api_client.request(method, url, data=dic)
        reslut =json.loads(rel.text)
        #print(reslut)
        self.assertEqual(reslut.get('totalCount'),12)


    def test_two(self):
        #self.skipTest('1111')
        test_one = self.test_list[1]
        method = extract_str_from_filed('request.method', test_one)
        url = extract_str_from_filed('request.url', test_one)
        data_dic = extract_str_from_filed('request.data', test_one)
        dic = tmpFunc(data_dic)
        rel =self.api_client.request(method, url, data=dic)
        reslut =json.loads(rel.text)
        #print(reslut)
        self.assertEqual(reslut.get('totalCount'),61)




# if __name__ == '__main__':
#     unittest.main(verbosity=0)