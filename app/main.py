from flask import Flask, request, render_template, session, jsonify
from datetime import timedelta
import json
import os
import modules.functions
import modules.mysql_connection
import modules.mongo_connection
import modules.address_book

# __name__ 用來 application 的相對位置
# 若是直接啟動的程式 __name__ 為 '__main__'
# 若是被滙入， __name__ 會是被滙入的名稱
app = Flask(
    __name__, 
    static_url_path = '/',
    static_folder = './static',
    template_folder ='./templates'
    )

app.config['SECRET_KEY'] = os.urandom(24)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=60)

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

@app.route('/params/')
@app.route('/params/<action>/')
@app.route('/params/<action>/<int:id>')
def my_params(action='none', id=0):
    return ( {
        'action': action,
        'id': id
    } )


@app.route('/try-session')
def try_session():
    if not session.get('what'):
        session['what'] = 1
    else:
        session['what'] += 1
    return str( session.get('what') )

@app.route('/try-mysql')
def try_mysql():
    (cursor, cnx) = modules.mysql_connection.get_cursor()
    sql = ("SELECT * FROM address_book")
    cursor.execute(sql)
    return render_template('data_table.html', t_data=cursor.fetchall())

@app.route('/try-mysql2')
def try_mysql2():
    (cursor, cnx) = modules.mysql_connection.get_cursor()
    sql = ("SELECT * FROM address_book")
    cursor.execute(sql)
    return jsonify(cursor.fetchall())

@app.route('/receive-json', methods=['POST'])
def receive_json():
    (cursor, cnx) = modules.mysql_connection.get_cursor()
    data = json.loads(request.get_data())  # JSON 字串轉換為 dict
    p = {}
    sids = []  # 用來記錄新增的 primary key
    p['name'] = data['name'] if 'name' in data else ''
    p['email'] = data['email'] if 'email' in data else ''
    p['mobile'] = data['mobile'] if 'mobile' in data else ''
    p['birthday'] = data['birthday'] if 'birthday' in data else '1900-01-01'
    p['address'] = data['address'] if 'address' in data else ''

    # 兩種作法
    sql1 = ("INSERT INTO `address_book`"
        "(`name`, `email`, `mobile`, `birthday`, `address`, `created_at`"
        ") VALUES (%s, %s, %s, %s, %s, NOW())")
    sql2 = ("INSERT INTO `address_book`"
        "(`name`, `email`, `mobile`, `birthday`, `address`, `created_at`"
        ") VALUES (%(name)s, %(email)s, %(mobile)s, %(birthday)s, %(address)s, NOW())")

    cursor.execute(sql1, (p['name'], p['email'], p['mobile'], p['birthday'], p['address']))
    sids.append(cursor.lastrowid)  # 取得新增項目的 primary key
    cursor.execute(sql2, p)  # 使用 dict
    sids.append(cursor.lastrowid)
    cnx.commit()  # 提交新增的資料才會生效

    return jsonify(sids)  # 輸出 JSON 格式


@app.route('/try-mongo')
def try_mongo():
    (db, c) = modules.mongo_connection.getDB('test')
    one = db.inventory.find_one()
    one['_id'] = str(one['_id'])  # 將 ObjectId 轉換為字串顯示
    return one

app.add_url_rule('/address-book/list/', None, modules.address_book.ab_list)
app.add_url_rule('/address-book/list/<int:page>', None, modules.address_book.ab_list)
