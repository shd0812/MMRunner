from Basc_Http import  Base_Requests
from  utils import get_Param,input_parm
from utils import open_Yaml

def xx_post(url,**kwargs):
    method = 'POST'
    host = 'https://mi.shaxiaoseng.com:4433/Xeenho/'
    client = Base_Requests(method, host, url)

    result=client.sxs_Api(data=kwargs)
    return result

def register_query(url,path):
    dic = get_Param(path)
    print('参数%s' % dic)
    result=xx_post(url,data=dic)
    return result

def send_post(parm_url,str):
    dic = input_parm(str)
    if dic =='输入参数不合法':
        return dic
    else:
        result=xx_post(parm_url,data=dic)
        return result

if __name__=='__main__':
    #path='C:/Users/shd/Desktop/测试文档/星火投资/星火脚本/用例/新用户注册.yaml'
    #data=register_query('register',path)
    parm_str = 'platform_uid=3000000419294000_m'
    data=send_post('query_useraccount',parm_str)
    print(data.text)

