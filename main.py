import function
import time
if __name__ == "__main__":

    ser = function.setting()
    fig, ax, line1, data_y1 = function.draw_setting()
    while 1:
        function.loop(ser, fig, line1, data_y1)
