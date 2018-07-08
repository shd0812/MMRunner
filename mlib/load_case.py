from mlib.utils import Operate_File
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
    result = TestLoad.load_file('../data/test_one/test_one.yaml')
    #print(result)
    #print(result[0]['validate'])
    tmp_list = result[0]['validate']
    for itme in tmp_list:
        print(itme)