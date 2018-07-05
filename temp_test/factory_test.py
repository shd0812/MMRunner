import unittest
import os,json,time
import HTMLTestRunner

class Test(unittest.TestCase):
    '测试类'
    #token_1 = token_emba('12012341006', '123456') #类变量
    def begin_req(self,apidata):
        u'获取部门列表'
        # print apidata
        if apidata[1] == ['']:
            data = eval(apidata[0])()
        elif apidata[1] != ['']:
            data = eval(apidata[0])(apidata[1])  # 输入要测试的数据,data=(mode,url,body),
       # back = json.loads(req(data, self.token_1)['res_body'])  # 获取实际返回值,需要传入token的话,请req(data,token)
        back = {
            'code':200
        }
        YQ = 200  # 输入预期的值
        SJ = back['code']  # 设置实际返回,如果需要传入TOKEN等header,请务必填写!
        self.assertEqual(200, SJ)

def demo(apidata):
    def tool(self):
        Test.begin_req(self,apidata)
    setattr(tool, '__doc__', u'测试%s' % str(apidata[0]))
    print(tool.__doc__)
    return tool


def testall(apidata):
    for i in range(len(apidata)):
     setattr(Test,'test_'+str(i+1),demo(apidata[i]))


if __name__ == "__main__":
    fname = './case_2.xls'
    Apidata = ['登录','退出']  #设置接口函数名


    testall(Apidata)
    suit = unittest.makeSuite(Test)
    now = time.strftime("%Y-%m-%M-%H_%M_%S", time.localtime(time.time()))
    # reports_dir_path = "..\\reports\\"  #'D:\Python\flask_mock\reports'
    reports_dir_path = "reports\\"  # D:\Python\flask_mock\API_Unitest\reports
    if not os.path.isdir(reports_dir_path):
        os.mkdir(reports_dir_path)
    filename = reports_dir_path + now + 'result.html'  # 定义个报告存放路径，支持相对路径。
    #fp = file(filename, 'wb')
    with open(filename, 'wb') as f:
        runner = HTMLTestRunner.HTMLTestRunner(stream=f, title='111111', description ='2222')
        runner.run(suit)