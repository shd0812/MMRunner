from mlib.utils import Operate_File,query_json
from mlib import m_expection
from mlib.logger import myLog
import json
logger =myLog.getLog()


class TestLoad():

    @staticmethod
    def load_file(path):

        oper = Operate_File(path)
        file_data=oper.read_file()
        logger.m_info('get the file_data：{}'.format(file_data))
        test_list= []
        if not isinstance(file_data,list):
            raise m_expection.FileFormatError("API format error: {}".format(path))

        for list_item in file_data:
            logger.m_info('get the item：{}'.format(list_item))
            if not isinstance(list_item, dict) or len(list_item) != 1:
                raise m_expection.FileFormatError("API format error: {}".format(path))
            else:
                try:

                    test_list.append(list_item['test'])
                except :
                    raise m_expection.ParamsError('额偶，出错了，因为{}'.format(list_item.get('test')))
        return test_list

if __name__ == '__main__':
    result = TestLoad.load_file('../data/test_one/demo_api.yaml')
    test_one = result[0]
    print(test_one)
    data_dic = query_json('request.data', test_one)
    for k,v in data_dic.items():
        if v.startswith('$'):
            print('1111')
            print(v)
    print(data_dic)