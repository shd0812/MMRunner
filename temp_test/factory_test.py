import unittest
import os,json,time
import HTMLTestRunner

class Test(unittest.TestCase):
    '测试类'
    #token_1 = token_emba('12012341006', '123456') #类变量
    def begin_req(self,apidata):
        u'获取部门列表'
        print (apidata)
        print(33333333)
def demo(apidata):
    print(apidata)
    def tool(self):
        #print(222222)
        Test.begin_req(self,apidata)
    setattr(tool, '__doc__', u'测试%s' % str(apidata[0]))
    print('hahaha%s'%__doc__)
    return tool



def testall(apidata):
    nameList = []
    for i in range(len(apidata)):
        name = 'test_' + str(i + 1)
        setattr(Test, name, demo(apidata[i]))
        nameList.append(name)
    return nameList


def suite(apidata):

    nameList = testall(apidata)
    print(nameList)
    suites =unittest.TestSuite()
    for i in nameList:
        suites.addTest(Test(i))
    return suites
def run(apidata):
    now = time.strftime("%Y-%m-%M-%H_%M_%S", time.localtime(time.time()))
    reports_dir_path = "reports\\"  # D:\Python\flask_mock\API_Unitest\reports
    if not os.path.isdir(reports_dir_path):
        os.mkdir(reports_dir_path)
    filename = reports_dir_path + now + 'result.html'  # 定义个报告存放路径，支持相对路径。
    with open(filename, 'wb') as f:
        runner = HTMLTestRunner.HTMLTestRunner(stream=f, title='111111', description='2222')
        runner.run(suite(apidata))



if __name__ == "__main__":
    apidata = ['登录','退出']  #设置接口函数名
    run(apidata)


