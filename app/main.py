from flask import Flask
from flask import request  # 滙入 request
from flask import render_template
import json
import modules.functions

# __name__ 用來 application 的相對位置
# 若是直接啟動的程式 __name__ 為 '__main__'
# 若是被滙入， __name__ 會是被滙入的名稱
app = Flask(__name__, '/')


# decorators 後面定義的 function 會變成 decorators 的參數
# 類似 JavaScript 的 callback function
@app.route('/')
def index():
    return '<h2>哈囉 Flask</h2>'


@app.route('/save-headers')
def save_headers():
    dict1 = {
        'cookies': {}
    }
    for i in request.headers:
        print(i)  # 查看取出的 headers 資料
        dict1[i[0]] = i[1]
    # 查看 cookies
    for i in request.cookies:
        dict1['cookies'][i] = request.cookies[i]
    file1 = open('headers.json', 'w')
    file1.write(json.dumps(dict1))  # 存成 JSON
    return dict1


# 語法：add_url_rule(rule, endpoint=None, view_func=None, provide_automatic_options=None, **options)
app.add_url_rule('/show-cookies', 'show-cookies', modules.functions.show_cookies)
# app.add_url_rule('/show-cookies', 'show-cookies')
# app.view_functions['show-cookies'] = modules.functions.show_cookies

@app.route('/basic-template')
def basic_template():
    return render_template('basic.html', name='是在哈囉', age=25)

@app.route('/basic-template2')
def basic_template2():
    output = {
        'name': '小明',
        'age': 30
    }
    return render_template('basic.html', ** output)


@app.route('/try-qs')
def queryString():
    # query string 轉成 dict
    # http://localhost:5000/try-qs?a[]=1&b=34&a[]=5
    output = {
        'args': request.args,
        'a[]': request.args.getlist('a[]'),
        'get_b': request.args.get('b'), 
        'get_a[]': request.args.get('a[]'), 
    }
    return output 

@app.route('/try-post', methods=['POST'])  # 限定使用 POST
def try_post():
    # 表單資料 urlencoded, form-data 皆可, 使用 postman 測試
    output = {
        'form': request.form,
        'a[]': request.form.getlist('a[]'),
        'post_b': request.form.get('b'), 
        'post_a[]': request.form.get('a[]'), 
    }
    return output
    
@app.route('/try-post2', methods=['POST'])
def try_post2():
    # 使用 postman post json 資料: {"a":11,"b":22}
    output = {
        'content_type': request.content_type,
        'data': request.data.decode('utf-8'),
        'json': request.get_json(),
    }
    return output

