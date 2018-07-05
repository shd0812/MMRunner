import os
from yaml import  load
from configparser import ConfigParser
import json
import platform
from mlib.logger import  myLog
from mlib.m_expection   import *
logger = myLog.getLog()
# 操作文件类
class operate_File():

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
    def write_file(self,text):
        with open(self.get_path(),'w') as pf:
            pf.write(text)

def valite_type(filed):
    if isinstance(filed,list):
        return 'l'
    elif isinstance(filed,dict):
        return 'd'
    elif isinstance(filed,str):
        return 's'
    elif isinstance(filed,int):
        return 'i'
    else:
        msg = '不识别该filed类型{}'.format(filed)
        logger.m_error(msg)
        raise ParamsError(msg)

def extract_str_from_filed(p_str,filed):

    if not  p_str:
        err_msg = u"Failed to find p_str!\n"
        raise ParamsError(err_msg)
    if not filed:
        err_msg = u"Failed to find filed!\n"
        raise ParamsError(err_msg)
    if valite_type(filed) !='d':
        err_msg = u"filed not dict!\n"
        raise ParamsError(err_msg)

    if '.' in p_str:
        item_list = p_str.split('.')
        tmp= filed
        for x in range(len(item_list)):
            result_data = item_list[x]
            if valite_type(tmp)=='d':
                tmp=tmp.get(result_data)
                if not tmp:
                    logger.m_error('参数可能出错了，参数为:{}'.format(result_data))
            elif valite_type(tmp)=='l':
                tmp=tmp[int(result_data)]
        return tmp
    else:
        return filed.get(p_str)




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

    print(extract_str_from_filed(p_str,check_data))




