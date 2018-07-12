import os
from yaml import  load
from configparser import ConfigParser
import json
from  copy import copy
import hashlib
import platform
from requests.structures import CaseInsensitiveDict
from mlib.logger import  myLog
from mlib.build_in import do_validation
from mconf.setting import PARAM_PATH
from collections import OrderedDict
from mlib.m_expection   import *
import re
logger = myLog.getLog()

variable_regexp = r"\$([\w_]+)"

#获取可变参数
def extract_variables(content):
    """ extract all variable names from content, which is in format $variable
    @param (str) content
    @return (list) variable name list

    e.g. $variable => ["variable"]
         /blog/$postid => ["postid"]
         /$var1/$var2 => ["var1", "var2"]
         abc => []
    """
    try:
        result_list=re.findall(variable_regexp, content)
        return result_list[0]
    except TypeError:
        return []
# 操作文件类
class Operate_File():

    def __init__(self,file_name):
        if not file_name:
            logger.m_error('文件名不能为空,文件名为{}'.format(file_name))
        else:
            self.file_name=file_name
    #获取路径
    def get_path(self):
        path=os.path.dirname( __file__)
        parent_path=os.path.dirname(path)
        grand_path=os.path.join(parent_path,self.file_name)
        if platform.system() == 'Windows':
            logger.m_debug('系统为windows')
            if '\..' in grand_path:
                final_path=grand_path.replace('\../','/')
                return final_path
        elif platform.system() == 'Linux':
            if '/../' in grand_path:
                final_path = grand_path.replace('/../','/')

                logger.m_debug('linux上地址为{}'.format(grand_path))
                return final_path
        else:
            logger.m_error('暂未考虑其他平台的处理')
    #读取文件
    def read_file(self):
        path=self.get_path()
        logger.m_debug('路径为{}'.format(path))
        if  'yaml'in self.file_name:
            try:
                with open(path, 'rb') as pf:
                    data=load(pf)
                return data
            except Exception as e:
                logger.m_error('读取出错了，{}'.format(e))
                return  e
        elif 'ini' in self.file_name:
            config=ConfigParser()
            try:
                config.read(path)
                return config
            except Exception as e:
                logger.m_error('读取出错了，{}'.format(e))
                return  e







def query_json(query,json_content,  delimiter='.'):
    """ Do an xpath-like query with json_content.
    @param (json_content) json_content
        json_content = {
            "ids": [1, 2, 3, 4],
            "person": {
                "name": {
                    "first_name": "Leo",
                    "last_name": "Lee",
                },
                "age": 29,
                "cities": ["Guangzhou", "Shenzhen"]
            }
        }
    @param (str) query
        "person.name.first_name"  =>  "Leo"
        "person.cities.0"         =>  "Guangzhou"
    @return queried result
    """
    if json_content == "":
        raise ResponseError("response content is empty!")

    try:
        for key in query.split(delimiter):
            if isinstance(json_content, list):
                json_content = json_content[int(key)]
            elif isinstance(json_content, (dict, CaseInsensitiveDict)):
                json_content = json_content[key]
            else:
                raise ParseResponseError(
                    "response content is in text format! failed to query key {}!".format(key))
    except (KeyError, ValueError, IndexError):
        raise ParseResponseError("failed to query json when extracting response!")

    return json_content

#解决接口参数依赖上个接口返回的问题
def assemble_parm(data_dic):
    if isinstance(data_dic,dict):
        for k, v in data_dic.items():
            if str(v).startswith('$'):
                logger.m_info('v是需要提替换%s'%v)
                tmp = fetch_extract()
                v=v[1:]
                logger.m_info('tmp为%s'%tmp)
                data_dic[k] = tmp[v]
    elif isinstance(data_dic,str):
        if '$' in data_dic:
            tmp = fetch_extract()#获取上个接口返回的参数，字典形式
            parm_str = extract_variables(data_dic)#提取参数
            new_str = tmp[parm_str]
            old_str='$'+parm_str
            data_dic = data_dic.replace(old_str,new_str)


        logger.m_info('最终结果为%s'%data_dic)
    return data_dic

# 提取依赖参数
def extract_response(query,response):
    if  not isinstance(query,list):
        raise ParamsError('1should be list')
    result_list = {}
    for item in query:
        if not isinstance(item, dict):
            raise ParamsError('2should be list')
        for k, v in item.items():

            #print('v是%s' %v)
            item[k] = query_json(v,response)
            result_list.update(item)

    return result_list


def keep_extract(result_list,response):
    if not isinstance(result_list,list):
        raise ParamsError('1should be list')
    e = extract_response(result_list, response)
    with open(PARAM_PATH, 'w') as f:
        f.write(json.dumps(e))
def fetch_extract():
    with open(PARAM_PATH, 'r') as f:
        result = f.read()
        content = json.loads(result)

        return content

# 从接口提取返回值，为做验证用
def validate_response(query,response):
    if  not isinstance(query,list):
        raise ParamsError('1should be list')
    result_list = []
    for item in query:
        if not isinstance(item, dict):
            raise ParamsError('2should be list')
        for k, v in item.items():
            tmp = copy(v)
            if not isinstance(v,list):
                raise ParamsError('3should be list')
            qe = v[0]

            tmp[0] = query_json(qe,response)
            tmp.insert(0,k)
            result_list.append(tmp)

    return result_list

# 验证期望值和返回值
def m_check(mapping):
    if  not isinstance(mapping,list):
        raise ParamsError('should be list')
    for item in mapping:
        s=do_validation(item[0],item[1],item[2])
        return s




#md5加密
def md5_str(str):
    b_str=bytes(str,encoding='utf-8')
    return hashlib.md5(b_str).hexdigest()

if __name__=='__main__':
    #op =operate_File('../TestData/gm/valid.yaml')
    #d=op.read_file()

    check_data={
            'test_name':'用户信息查询',
            'parm':{
                'service':'bind_url',
                'body':[{
                    'index':{
                        'name':'shen',
                        'vals':[111111,222222]
                    }
                    }]
                }

            }


    #op = operate_File('../data/test_one/extract')
    #op.write_file(json.dumps(check_data))

    p_str = 'parm.body.0.index.vals.1'

    #print(query_json(p_str,check_data))
    print(fetch_extract())




