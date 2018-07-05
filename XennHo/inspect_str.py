#coding:utf-8


result_list=[]
def inspect_lack(str,list):
    for key in list:
        if key in str:
            return
        else:
            print(key)
            result_list.append(key)
    print('缺少这些字段:%s' % result_list)
    return result_list

if __name__ =="__main__":
    str=''
    list=''
