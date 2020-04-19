from flask import Flask

# __name__ 用來 application 的相對位置
# 若是直接啟動的程式 __name__ 為 '__main__'
# 若是被滙入， __name__ 會是被滙入的名稱
app = Flask(__name__)

# decorators 後面定義的 function 會變成 decorators 的參數
# 類似 JavaScript 的 callback function
@app.route('/')
def index():
    return '<h2>哈囉 Flask</h2>'
