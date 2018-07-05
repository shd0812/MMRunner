from flask import Blueprint
from flask import render_template,request
from XennHo.test import send_post
from flask import jsonify

xnho = Blueprint('xnho', __name__)


@xnho.route('/', methods=['GET', 'POST'])
def home():
    return render_template('xhzt.html')

@xnho.route('/next', methods=['GET', 'POST'])
def next():
    print(1111)
    print(request.method)
    #type = request.form['apitype']
    parm_str=request.form['parm_str']
    parm_url = request.form['parm_url']
    data = send_post(parm_url, parm_str)
    # list_dic={}
    # list_dic['result']=str(data)
    # print('返回结果:%s' % list_dic)
    return jsonify(data)