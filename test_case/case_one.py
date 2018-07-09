from mlib.m_client import HttpSession
from mlib.utils import  *
from  XennHo.utils import input_parm



def tmpFunc(p_dic):
    for var_k, var_v in p_dic.items():
        result = var_k + '=' + var_v
        result = input_parm(result)
        #print(result)
        return result

def run_single_testcase(testcase):
    api_client = HttpSession('https://mi.shaxiaoseng.com:4433/Xeenho/')
    if type(testcase) != dict:
        testcase = eval(testcase)
    method = query_json('request.method', testcase)
    url = query_json('request.url', testcase)
    data_dic = query_json('request.data', testcase)
    v_list = testcase['validate']
    dic = tmpFunc(data_dic)

    rel = api_client.request(method, url, data=dic)
    response = eval(rel.text)
    r = extract_response(v_list, response)
    return r
