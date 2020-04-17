import mysql.connector as mysql
import sys
import Adafruit_DHT
from datetime import datetime

def insert_values(sensor_id,temp,hum):
    dt=datetime.now()
    conn=mysql.connect(host="10.42.0.1",user="root",passwd="159159",database="test1")
    curs=conn.cursor()
    query="INSERT INTO sensor_data(date_time,sensor_id,temp,hum) values(NOW(),%s,%s,%s)"
    values=(sensor_id,temp,hum)
    curs.execute(query,values)
    conn.commit()
    conn.close()


hum,temp=Adafruit_DHT.read_retry(Adafruit_DHT.AM2302,17)

if hum is not None and temp is not None:
    id1="1"
    insert_values(id1,temp,hum)
else:
    print("Error while reading")
