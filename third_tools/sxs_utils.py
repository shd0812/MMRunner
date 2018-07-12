from mlib.m_expection import *
from third_tools.encry_sxs import encryt_sxs,decrypt_sxs
from mlib.logger import myLog

logger = myLog.getLog()
#拼装加密前的数据
def before_encry_sxs(dic):
    """
    data={
      'mobile':'13521137791',
      'passwd':'123456'
    }
    :param dic:
    :return: mobile=13521137791&passwd=123456
    """
    if not isinstance(dic,dict):
        raise  TypeError
    result=''
    for k,v in dic.items():
        tmp = k +'='+v
        result += '&'+tmp
    if result.startswith('&'):
        re=result.replace('&','',1)
        logger.m_info('加密前数据为{}'.format(re))
        return re


# 获取加密后最终的data
def after_encry_sxs(encry_str):
    if not isinstance(encry_str,str):
        raise ParamsError('加密字符应该是字符串，但是现在确是{}{}'.format(encry_str,type(encry_str)))

    data_dic = {'data':encry_str}
    logger.m_info('加密后最终的data{}'.format(data_dic))
    return data_dic

# 获取加密秘钥和解密秘钥
def get_seeds(token):
    if not isinstance(token,str):
        raise ParamsError('加密字符应该是字符串，但是现在确是{}{}'.format(token,type(token)))
    encrypt_seed = token[6:14]
    decrypt_seed = token[14:21]
    return encrypt_seed, decrypt_seed
# 加密
def encry_data(data,token): #U0Zhd29TeSNSQ2QragR8c1dAZH1qBXx2V0dkf2oFfHZXRWV5bgB4dVJDYH1uBXhxUkJkK2oEfHdXR2R+agR8dw==
    seeds = get_seeds(token)
    encrypt_seed = seeds[0]
    res = encryt_sxs(data, encrypt_seed)
    logger.m_info('加密结果为{}'.format(res))
    return res
#解密
def decry_data(data,token):
    seeds = get_seeds(token)
    encrypt_seed = seeds[1]
    res = decrypt_sxs(data, encrypt_seed)
    return res
