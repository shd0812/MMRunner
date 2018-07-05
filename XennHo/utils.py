from yaml import  load
import os
from  XennHo.aseEncry import prpcrypt,Sign

def open_Yaml(path):
    with open(path,'rb') as pf:
        data=load(pf)
        return data['testcase']

# 读取yaml来获取加密参数
def get_Param(path):
    pc = prpcrypt()
    ss=Sign()
    data=open_Yaml(path)

    s={}
    d={}
    for list in data:
        if list['encry']==1:
            for s_key in list:
                if s_key =='t_code':
                    list[s_key]=ss.getTimestamp()
            for key in list:
                if key != 'encry':
                    s[key] = list[key]
                    list[key]=pc.encrypt(str(list[key]))

                    d[key] = list[key]
        else:
            for key in list:
                if key!='encry':
                    s[key] = list[key]
                    d[key]=list[key]
    #print(s)
    serial_num=s['serial_num']
    c_code=s['c_code']
    t_code=s['t_code']
    # print('sign时间戳%s' % t_code)
    #print(serial_num,t_code,c_code)
    sign=ss.get_sign(serial_num,str(t_code),c_code)
    d['sign']=sign

    return d
# 通过网页输入来获取
def input_parm(parm_str):
    ss = Sign()
    if '&' in parm_str or '=' in parm_str or parm_str=='_m':
    #parm_str='platform_uid=293_m&start_time=2018-05-12 12:34:34&end_time=2018-05-12 12:34:34'
        m_code='shaxiaoseng_xhzt'
        c_code='c_code='+m_code+'_m&'
        m_t_code=str(ss.getTimestamp())+'000'
        t_code='t_code='+m_t_code+'_m&'
        m_serial_num='dddddddfff'
        serial_num='serial_num='+m_serial_num+'&'
        parm_str = c_code+t_code+serial_num+parm_str
        # print('输入参数为:%s' % parm_str)
        list = parm_str.split('&')
    #print(list)
        pc = prpcrypt()
        parm_dic = {}
        for child in list:
            child_list=child.split('=')
            #print(child_list)
            if '_m' in child_list[1]:
                child_list[1] = child_list[1][0:len(child_list[1])-2]
                child_list[1]=pc.encrypt(child_list[1])
                parm_dic[child_list[0]]=child_list[1]
            else:
                parm_dic[child_list[0]] = child_list[1]
        sign = ss.get_sign(m_serial_num,m_t_code,m_code)
        parm_dic['sign'] = sign
        # print('加密后的参数:%s' % parm_dic)
        return parm_dic

    else:
        return '输入参数不合法'


if __name__=='__main__':
    print(111)
    #data=get_Param('C:/Users/shd/Desktop/测试文档/星火投资/星火脚本/用例/用户投资记录查询.yaml')
    #print(data)
    parm_str='platform_uid=293_m&start_time=2018-05-12 12:34:34&end_time=2018-05-12 12:34:34'

    input_parm(parm_str)