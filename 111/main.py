import funtion
from flask import Flask, render_template
import time
import matplotlib.pyplot as plt


app = Flask(__name__)


@app.route('/')
def build_plot_index():
    db = funtion.Database()
    first_web, second_web, third_web, fourth_web = db.get_all_flow_plot()


    pie_flow = db.pie_flow_data()
    title = "flow"
    return render_template('test1.html', plot_first_flow=first_web,
                           plot_second_flow=second_web,
                           plot_third_flow=third_web,
                           plot_four_flow=fourth_web,
                           plot_url_pie= pie_flow,
                           title=title)


@app.route('/pressure')
def build_plot_pressure():
    """plt.close()
    first = funtion.Database(datalist="firstfloor")
    first_time, first_flow, first_pressure = first.get_sql_data()

    second = funtion.Database(datalist="secondfloor")
    second_time, second_flow, second_pressure = second.get_sql_data()

    third = funtion.Database(datalist="thirdfloor")
    third_time, third_flow, third_pressure = third.get_sql_data()
    img_pressure = first.get_img_pressure(first_pressure, second_pressure, third_pressure, first_time)

    title = "123"
    return render_template('test1.html', plot_url_pressure=img_pressure, title=title)
    """


if __name__ == '__main__':
    while True:
        app.debug = True
        start = time.time()
        app.run()
        end = time.time()
        time.sleep(3-(end - start))