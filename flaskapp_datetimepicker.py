import time
import datetime
import mysql.connector as mysql
from flask import Flask, render_template, request
import Adafruit_DHT

app = Flask(__name__)


@app.route("/")
def hello():
    hum, temp = Adafruit_DHT.read_retry(Adafruit_DHT.AM2302, 17)

    if hum is not None and temp is not None:
        return render_template("flaskapp.html", temp=temp, hum=hum)
    else:
        return render_template("no_sensor.html")


@app.route("/app_database", methods=['GET'])
def app_database():
    data, from_date_str, to_date_str = get_records()

    return render_template("app_database.html", data=data, temp_items=len(data), hum_items=len(data),
                           from_date=from_date_str, to_date=to_date_str)


def get_records():
    from_date_str=request.args.get('from',time.strftime("%Y-%m-%d %H:%M"))
    to_date_str= request.args.get('to',time.strftime("%Y-%m-%d %H:%M"))
    range_h_form = request.args.get('range_h')
    print("range_h_form value:", range_h_form)

    if range_h_form is not None:
        range_h_int = int(range_h_form)
        print("type of range_h_int:", type(range_h_int))
        print("range_h_int:", range_h_int)
        time_now = datetime.datetime.now()
        time_from = time_now - datetime.timedelta(hours=range_h_int)
        time_to = time_now

        from_date_str = time_from.strftime("%Y-%m-%d %H:%M")
        to_date_str = time_to.strftime("%Y-%m-%d %H:%M")

    elif range_h_form is None and from_date_str is None and to_date_str is None:
        range_h_form = "1"
        range_h_int = int(range_h_form)
        print("type of range_h_int:", type(range_h_int))
        print("range_h_int:", range_h_int)
        time_now = datetime.datetime.now()
        time_from = time_now - datetime.timedelta(hours=range_h_int)
        time_to = time_now
        from_date_str = time_from.strftime("%Y-%m-%d %H:%M")
        to_date_str = time_to.strftime("%Y-%m-%d %H:%M")

    elif from_date_str is not None and to_date_str is not None and range_h_form is None:
        if not validate_date(from_date_str):  # Validate date before sending it to the DB
            from_date_str = time.strftime("%Y-%m-%d 00:00")
        if not validate_date(to_date_str):
            to_date_str = time.strftime("%Y-%m-%d %H:%M")

    conn = mysql.connect(host="10.42.0.1", user="root", passwd="159159", database="test1")
    curs = conn.cursor()
    curs.execute("SELECT * FROM sensor_data where date_time between %s and %s", (from_date_str, to_date_str))
    data = curs.fetchall()
    print(data)
    conn.close()
    return [data, from_date_str, to_date_str]

def validate_date(d):
    try:
        datetime.datetime.strptime(d, '%Y-%m-%d %H:%M')
        return True
    except ValueError:
        return False


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

