import mysql.connector

connect_data = {
    'host': 'localhost',
    'user': 'root',
    'passwd': 'root',
    'database': 'test'
}
cnx = None

def get_connection():
    global cnx  # 將連線物件存放在全域變數
    if not cnx:
        cnx = mysql.connector.connect(**connect_data)
        return cnx
    else:
        return cnx

def get_cursor():
    return get_connection().cursor(dictionary=True)  # 讀出資料使用 dict，預設為 tuple
