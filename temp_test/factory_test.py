from mlib.m_client import HttpSession

from  XennHo.utils import input_parm
from mlib.load_case import TestLoad
from mlib.utils import  *
import unittest,json


def tmpFunc(p_dic):
    for var_k, var_v in p_dic.items():
        result = var_k + '=' + var_v
        result = input_parm(result)
        #print(result)
        return result

result = TestLoad.load_file('../data/test_one/demo_api.yaml')
print(json.dumps(result))
test_list = result[1]
v_list = test_list['validate']
#print(v_list)
api_client = HttpSession('https://mi.shaxiaoseng.com:4433/Xeenho/')
test_one = test_list

method = query_json('request.method', test_one)
url = query_json('request.url', test_one)
data_dic = query_json('request.data', test_one)

dic = tmpFunc(data_dic)
rel = api_client.request(method, url, data=dic)

response = eval(rel.text)

print(response)


