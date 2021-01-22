import mysql.connector
from mysql.connector import Error

try:
    connection = mysql.connector.connect(host='localhost',
                                         database='test',
                                         user='root',
                                         password='123456')
    # 使用cursor()方法取得操作指標
    cursor = connection.cursor()

    # 使用execute方法執行sql陳述式
    cursor.execute("SELECT VERSION()")

    # 使用 fetchone() 方法取得一條資料
    data = cursor.fetchone()
    for i in data:
        print("Database version : %s " % i)

    connection.close()  # 關閉資料庫連線

except Error as e:
    print("Error reading data from MySQL table", e)
