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
    cursor = get_connection().cursor(dictionary=True)  # 讀出資料使用 dict，預設為 tuple
    return (cursor, get_connection())  # 同時回傳 cursor 和 connection
