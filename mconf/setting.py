import os
BASE_PATH = os.path.dirname(   #找到utp的目录
    os.path.dirname(os.path.abspath(__file__))
)

"""
 配置所有的文件
"""


MAIL_HOST='smtp.163.com'
MAIL_USER='lix.xxxx@163.com'
MAIL_PASSWRD = 'xxxxxxxxx1'
TO = [
    '5472xxxxx@qq.com',
]
LEVEL = 'error' #日志级别 info,debug,warning,critical,error


LOG_PATH = os.path.join(BASE_PATH,'logss') #存放日志的路径
CASE_PATH = os.path.join(BASE_PATH,'cases') #存放用例的路径
YAML_PATH = os.path.join(BASE_PATH,'case_data') #存放yaml文件的路径
CASE_TEMPLATE = os.path.join(BASE_PATH,'conf','base.txt') #用例模板的路径
REPORT_PATH = os.path.join(BASE_PATH,'report') #存放报告的目录
REPORT_TITLE ='星火的'
REPORT_DESCRIPTION = '本次为星火的项目'
BASE_URL = 'http://118.xx.xx.xx' #接口的地址