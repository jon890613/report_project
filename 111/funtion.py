import mysql.connector
import numpy as np
import pandas as pd
from mysql.connector import Error
import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt  # 資料視覺化套件
import io
import base64


class Database(object):
    """
    初始化(init) 預設 host = localhost
                     database=esp8266
                     user=root
                     password=None
    ------------------------------------
            需輸入   datalist
    """

    def __init__(self, host="localhost", database="esp8266", user="root", password="123456"):
        self.host = host
        self.database = database
        self.user = user
        self.password = password

    """
    功能:連線資料庫，並輸入資料庫指令取得最後100筆資料
    """

    def get_sql_data(self, data_list, field=None):
        try:
            connection = mysql.connector.connect(host=self.host,  # 資料庫IP位址
                                                 database=self.database,  # 資料庫名稱
                                                 user=self.user,  # 登錄帳號
                                                 password=self.password)  # 登錄密碼
            cursor = connection.cursor()

            if field:
                # cursor.execute(f"select {field}, datetime from {data_list} order by id desc limit 100;")
                cursor.execute(f"select {field}, datetime from {data_list};")
            else:
                cursor.execute(f"select * from {data_list} order by datetime desc limit 100;")  # 指令

            # cursor.execute(f"select * from {self.datalist} order by datetime asc limit 10, 5 ;")  # 抓最後10筆資料
            data = cursor.fetchall()  # 取得回傳資料
            connection.close()  # 關閉資料庫
            return data  # 回傳結果

        except Error as e:  # 如發生異常顯示錯誤訊息
            print("Error reading data from MySQL table", e)

    """
    分別將數據提出來(time, flow, pressure)
    """

    def conversion_data(self, data):
        data_array = np.array(data)  # 將資料轉換成陣列型態
        img_data = data_array[::-1]  # reverser
        data_re = img_data.T  # 翻轉
        now_time = data_re[3]  # 取時間
        flow = data_re[1]  # 取出flow數據
        pressure = data_re[2]  # 取出pressure數據
        str_x = []  # 建立空的時間 list

        """
        將時間格式(datatime.datatime)轉換成字串(str)
        """
        for j in now_time:
            a = str(j)
            str_x.append(str(a[-9:]))

        return str_x, flow, pressure  # 回串時間字串、flow、pressure

    def conversion_flow_data(self, data):
        data_array = np.array(data)  # 將資料轉換成陣列型態
        img_data = data_array[::-1]  # reverser
        data_re = img_data.T  # 翻轉
        now_time = data_re[1]  # 取時間
        flow = data_re[0]
        str_x = []

        for j in now_time:
            a = str(j)
            str_x.append(str(a[-9:]))

        return flow, str_x

    """
    資料視覺化(flow折線圖)
    """

    def get_img_flow(self, flow, time_re):
        img_index = io.BytesIO()
        plt.plot(time_re, flow, color='blue')
        plt.xticks(rotation=25)
        plt.ylim((0, 300))
        plt.xlim((0, 20))
        plt.savefig(img_index, format='png')
        plt.grid(True)  # 顯示虛線
        img_index.seek(0)
        plot_url_index = base64.b64encode(img_index.getvalue()).decode()
        plt.close()
        return plot_url_index

    """
    資料視覺化(pressure折線圖)
    """

    def get_img_pressure(self, first_flow, second_flow, third_pressure, time_re):
        img_pressure = io.BytesIO()
        plt.plot(time_re, first_flow, color='red')
        plt.plot(time_re, second_flow, color='blue')
        plt.plot(time_re, third_pressure, color='green')

        plt.grid(True)  # 顯示虛線
        plt.xticks(rotation=20)
        plt.savefig(img_pressure, format='png')
        img_pressure.seek(1)
        plot_url_pressure = base64.b64encode(img_pressure.getvalue()).decode()
        return plot_url_pressure

    """
    資料視覺化(flow圓餅圖)
    """

    def pie_flow_data(self):
        db = Database()
        first, second, third, fourth = db.get_all_data(field="flow")
        first_data, second_data, third_data, fourth_data = db.con_all_flow_data(first, second, third, fourth)

        img_pie_flow = io.BytesIO()
        first_total = sum(first_data)
        second_total = sum(second_data)
        third_total = sum(third_data)
        fourth_total = sum(fourth_data)
        miss = fourth_total - first_total - second_total - third_total
        sizes = [first_total, second_total, third_total, miss]
        labels = 'First', 'Second', 'Third', 'miss'
        plt.pie(sizes, labels=labels)
        plt.axis('equal')
        plt.savefig(img_pie_flow, format='png')
        img_pie_flow.seek(0)
        plot_url_pie = base64.b64encode(img_pie_flow.getvalue()).decode()
        plt.close()
        return plot_url_pie

    def web_flow_img(self, first):
        db = Database()
        first_time, first_flow, first_pressure = db.conversion_data(first)
        first_img_index = db.get_img_flow(first_flow, first_time)

        return first_img_index

    def get_all_data(self, field=None):
        db = Database()
        first = db.get_sql_data("firstfloor", field)
        second = db.get_sql_data("secondfloor", field)
        third = db.get_sql_data("thirdfloor", field)
        fourth = db.get_sql_data("fourthfloor", field)

        return first, second, third, fourth

    def get_all_flow_plot(self):
        db = Database()
        first, second, third, fourth = db.get_all_data()
        first_web = db.web_flow_img(first)

        second_web = db.web_flow_img(second)

        third_web = db.web_flow_img(third)

        fourth_web = db.web_flow_img(fourth)

        return first_web, second_web, third_web, fourth_web

    def con_all_flow_data(self, first, second, third, fourth):
        db = Database()
        first_data, time = db.conversion_flow_data(first)
        second_data, time = db.conversion_flow_data(second)
        third_data, time = db.conversion_flow_data(third)
        fourth_data, time = db.conversion_flow_data(fourth)

        return first_data, second_data, third_data, fourth_data
