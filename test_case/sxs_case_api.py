from mlib.m_client import HttpSession
from mlib.utils import  *
from third_tools.sxs_utils import before_encry_sxs,after_encry_sxs,encry_data,decry_data

import json
from mlib.load_case import TestLoad
from mlib.logger import myLog

logger = myLog.getLog()



# for item in result:



def run_single_testcase(testcase):
    api_client = HttpSession('https://ts.shaxiaoseng.com:4433/Api2/Api.php')
    if type(testcase) != dict:
        testcase = eval(testcase)
    method = query_json('request.method', testcase)
    url = query_json('request.url', testcase)
    url = assemble_parm(url)
    auth_key =query_json('request.encry',testcase)
    data_dic = query_json('request.data', testcase)
    v_list = testcase['validate']
    data_dic = assemble_parm(data_dic)
    if auth_key ==0:
        dic = data_dic
    else:
        before_str = before_encry_sxs(data_dic)
        auth_key = assemble_parm(auth_key)
        logger.m_info('获取的key为:{}'.format(auth_key))
        after_str = encry_data(before_str, auth_key)
        dic = after_encry_sxs(after_str)

    rel = api_client.request(method, url, data=dic)
    response = eval(rel.text)

    extract_list = query_json('request.extract',testcase)
    if extract_list:
        keep_extract(extract_list,response)
    if auth_key !=0:
        response= decry_data(str(query_json('Key',response)),auth_key)
        response = json.loads(response)
    r = validate_response(v_list, response)
    return r

if __name__ == '__main__':
    result = TestLoad.load_file('../data/test_one/sxs_api.yaml')
    test_case1 = result[0]
    for test_case in result:
        t=run_single_testcase(test_case)
        print(t)