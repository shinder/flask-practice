## 建立 Flask 專案

本文的參考專案 [https://github.com/shinder/flask-practice](https://github.com/shinder/flask-practice)，本部落格 [qops](https://qops.blogspot.com/)

首先如之前的文章 [建立專案](https://qops.blogspot.com/2019/10/python.html)。

``` bash
md flask-practice #建立專案資料夾
cd flask-practice #到專案目錄
python3 -m venv venv #安裝虛擬環境
source venv/bin/activate #啟動虛擬環境(mac)
```

安裝 Flask：

``` bash
pip install flask
```

可以使用下列兩個命列中的一個查看安裝的套件：

``` bash
pip list
pip freeze
```

建立 app 資料夾，用來存放自己撰寫的程式，並在裡面建立 main.py

``` python
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
```

在專案目錄建立執行的 run.sh，在 mac 記得將檔案屬性設定為 +x 可執行：

``` bash
# mac
export FLASK_APP=app/main.py
export FLASK_ENV=development
flask run --host=localhost --port=5000

# windows
# set FLASK_APP=app/hello.py
# set FLASK_ENV=development
# flask run
```

在 terminal 執行 run.sh，並在瀏覽器拜訪 localhost:5000 即可看到我們的第一個頁面。


