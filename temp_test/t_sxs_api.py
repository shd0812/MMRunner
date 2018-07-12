from mlib.m_client import HttpSession
from third_tools.sxs_utils import *
from mlib.utils import *
client = HttpSession('https://ts.shaxiaoseng.com:4433/Api2/Api.php')
method = 'post'
# mid = '238212'
# url = '/User/login/auth_id/%s' % mid
#
# passwd='111111'
# md5_pasd=md5_str(passwd)
# origin_data='phone=13373083974&userpwd=123456'
# encry_str=encry_data(origin_data,'kczQaz1r4sUedGRSi7E3Lo26L1r')
# print(encry_str)
# # encry_str = 'AQBufVlUWTMABWshXANcZQUFa3RcA1xnBQFrdFwDXGYFBWpzWAdYZQAFb3dYAlhhAARrIVwDXGcFAWt0XANcZw'
# data_dic = after_encry_sxs(encry_str)

# url='/Index/index'
# data_dic = {
#     'kid':'EC0B63850AFA384118DCCD9A9D8DBFDCED465601',
#     'source':'android',
#     'version':'1.4.5'
# }
#
#
# rel = client.request(method, url, data=data_dic)
# response = eval(rel.text)
# print(response)
import re
variable_regexp = r"\$([\w_]+)"


tmp ='$mid'


def extract_variables(content):
    """ extract all variable names from content, which is in format $variable
    @param (str) content
    @return (list) variable name list

    e.g. $variable => ["variable"]
         /blog/$postid => ["postid"]
         /$var1/$var2 => ["var1", "var2"]
         abc => []
    """
    try:
        result_list=re.findall(variable_regexp, content)
        return result_list[0]
    except TypeError:
        return []
e_str = extract_variables(tmp)
old_str = '$'+e_str
print(tmp)
s=tmp.replace(old_str,'310')
print(s)




