import matplotlib.pyplot as plt
import numpy as np
import serial

'''
    setting()
    設定arduino與python的連接
    還有創立圖表需要的x軸與y軸
'''


def setting():
    COM_PORT = 'COM3'  # 指定通訊埠名稱
    BAUD_RATES = 300  # 設定傳輸速率
    ser = serial.Serial(COM_PORT, BAUD_RATES)

    return ser


def cal(x, y, z):
    if x != (y + z):
        print("Exception Handling")

    else:
        print("Working normally....")


def draw_setting():
    fig = plt.figure()
    ax = fig.add_subplot(111)
    x = np.linspace(0, 23, 23)
    y = [0 for i in range(23)]
    plt.ion()
    line1, = ax.plot(x, y, 'b-')

    plt.ylim(0, 100)
    data_y1 = np.zeros([1, 23])
    return fig, ax, line1, data_y1


def loop(ser, fig, line1, data_y1):
    count = 0
    while ser.in_waiting:
        if count == 23:
            count = 0

        data_raw = ser.readline()  # 讀取一行
        data = data_raw.decode()
        data_y1[0][count] = int(data)
        line1.set_ydata(data_y1)
        fig.canvas.draw()
        plt.pause(1)
        count += 1
