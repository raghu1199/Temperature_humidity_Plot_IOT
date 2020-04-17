import time
import datetime
import mysql.connector as mysql
from flask import Flask,render_template,request
import Adafruit_DHT

app = Flask(__name__)

@app.route("/")
def hello():

    hum,temp=Adafruit_DHT.read_retry(Adafruit_DHT.AM2302,17)

    if hum is not None and temp is not None:
        return render_template("flaskapp.html",temp=temp,hum=hum)
    else:
        return render_template("no_sensor.html")


@app.route("/app_database",methods=['GET'])
def app_database():
    data= get_records()
    return render_template("app_database.html",data=data)

def get_records():
    from_date_str=""
    to_date_str=""
    range_h_form=request.args.get('range_h',"")
    range_h_int="nan"
    try:
        range_h_int=int(range_h_form)
    except:
        print("range_h_form is not Number")

    if isinstance(range_h_int,int):
        time_now= datetime.datetime.now()
        time_from=time_now-datetime.timedelta(hours=range_h_int)
        time_to=time_now

        from_date_str=time_from.strftime("%Y-%m-%d %H:%M")
        to_date_str=time_to.strftime("%Y-%m-%d %H:%M")


    conn=mysql.connect(host="10.42.0.1",user="root",passwd="159159",database="test1")
    curs=conn.cursor()
    curs.execute("SELECT * FROM sensor_data where date_time between %s and %s",(from_date_str,to_date_str))
    data=curs.fetchall()
    conn.close()
    return data
    


if __name__=="__main__":
    app.run()

