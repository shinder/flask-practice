from flask import Flask
from flask import request  # 滙入 request
import json

# __name__ 用來 application 的相對位置
# 若是直接啟動的程式 __name__ 為 '__main__'
# 若是被滙入， __name__ 會是被滙入的名稱
app = Flask(__name__)


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
