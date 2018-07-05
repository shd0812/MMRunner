import requests
import json



class Base_Requests(object):
    def __init__(self, method, host, params_url):
        self.host = host
        self.method = method
        self.params_url = params_url

    def sxs_Api(self, **kwargs):
        url = self.host + self.params_url
        #print(kwargs)
        if self.method == 'POST':
            kwargs = kwargs['data']['data']
            #print(kwargs)
            r = requests.post(url, data=kwargs)

            r.encoding = 'UTF-8'
            if r.status_code == 200:
                result = r
                return result
        else:
            r = requests.get(url, params=kwargs)
            r.encoding = 'UTF-8'
            if r.status_code == 200:
                result = json.loads(r.text)
                return result



if __name__ == '__main__':
    method = 'POST'
    host = 'https://ts.shaxiaoseng.com:4433/Api2/Api.php/'
    url = 'Index'
    client = Base_Requests(method, host, url)

    dic={'key':'1','vault':'2'}
    client.sxs_Api(data=dic)