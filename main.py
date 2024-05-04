import RPi.GPIO as GPIO
import time
from datetime import datetime
import os
import json
from datetime import datetime
import board
import adafruit_dht
from flask import Flask,request,render_template
import threading
from hydro import Hydro
import sqlite3
from sqlite3 import Error

LIGHT_RELAY_PIN = 18  # Example GPIO pin
dhtDevice = adafruit_dht.DHT22(board.D4, use_pulseio=False)

# Setup GPIO
GPIO.setmode(GPIO.BCM)  # Use Broadcom pin-numbering scheme
GPIO.setup(LIGHT_RELAY_PIN, GPIO.OUT)

# Other vaiables
web_file_path = os.path.abspath('/home/chrisbezuidenhout/Documents/Hydro/web_data.txt') 
db_file_path = os.path.abspath('/home/chrisbezuidenhout/Documents/Hydro/HydroData.db') 



def create_connection(db_file):
    """Create a database connection to a SQLite database"""
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e+"\n")
    return conn

def create_table(conn):
    """Create a table if it doesn't already exist"""
    try:
        c = conn.cursor()
        c.execute("""CREATE TABLE IF NOT EXISTS hydro_data (
                     Date TEXT,
                     Time TEXT,
                     Humidity REAL,
                     Temperature REAL,
                     Light BOOLEAN
                     )""")
    except Error as e:
        print(e,"\n")

def write_data(date, time, humidity, temperature, light):
    """Insert a new entry into the hydro_data table"""
    conn = create_connection(db_file_path)
    if conn is not None:
        create_table(conn)
        conn.close()
    else:
        print("Error! cannot create the database connection\n")
    try:
        conn = create_connection(db_file_path)
        c = conn.cursor()
        c.execute("INSERT INTO hydro_data (Date, Time, Humidity, Temperature, Light) VALUES (?, ?, ?, ?, ?)",
                  (date, time, humidity, temperature, light))
        conn.commit()
        print("Data written successfully","\n")
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()

def get_current_date_and_time():
    current_time = str(datetime.now())[:16]
    current_hour = current_time[11:13]
    current_minute = current_time[14:]
    current_year = current_time[:4]
    current_month = current_time[5:7]
    current_day = current_time[8:10]
    return [current_day,current_month,current_year,current_hour,current_minute]

def get_climate_data():
    sensor_data = False
    while not sensor_data:
        try:
            temperature_c = dhtDevice.temperature
            humidity = dhtDevice.humidity
            try:
                if temperature_c and humidity:
                    sensor_data = True     
                else:
                    sensor_data = False
            except:
                print("getting the except issue")
            
        except RuntimeError as error:
            continue
        except Exception as error:
            dhtDevice.exit()
            raise error
    return (temperature_c,humidity)

def write_dict_to_file(data_dict):
    global web_file_path
    # Open the file in write mode
    with open(web_file_path, 'w') as file:
        # Serialize dict to a JSON formatted string and write it to the file
        json.dump(data_dict, file, indent=4)    

# def format_data(data_list,starting_date, ending_date):
def format_data(data_list):
    # date_difference_day = day_difference(starting_date,ending_date)
    # date_difference_month = month_difference(starting_date,ending_date)
    json_data_list=[]
    high_temp = -100
    low_temp = 100
    ave_temp = 0
    high_humid = -100
    low_humid = 100
    ave_humid = 0

    for row in data_list:
        row_date = row[0]
        row_time = row[1]
        row_humidity = row[2]
        row_temps = row[3]
        row_light = row[4]

        ave_temp += row_temps
        ave_humid += row_humidity

        if row_humidity > high_humid:
            high_humid = row_humidity

        if row_humidity < low_humid:
            low_humid = row_humidity

        if row_temps > high_temp:
            high_temp = row_temps

        if row_temps < low_temp:
            low_temp = row_temps

        json_obj = {
            "Date" : row_date,
    		"Time" : row_time,
    		"Humidity" : row_humidity,
    		"Temperature" : row_temps,
    		"Light" : row_light
        }
        json_data_list.append(json_obj)
    try:    
        ave_temp = round(ave_temp/len(json_data_list),2)
        ave_humid = round(ave_humid/len(json_data_list),2)
    except:
        ave_temp = 0 
        ave_humid = 0

    dataDictionary = {
        "chart": "bar",
        "data_summary":{
            "high_temp" : high_temp,
            "low_temp" : low_temp,
            "ave_temp" : ave_temp,
            "high_humid" : high_humid,
            "low_humid" : low_humid,
            "ave_humid" : ave_humid
        },
        "data": json_data_list
    }
    return dataDictionary

def get_data(start_date, end_date):
    """Retrieve data from hydro_data table between two dates"""
    conn = create_connection("HydroData.db")
    try:
        c = conn.cursor()
        query = "SELECT Date, Time, Humidity, Temperature, Light FROM hydro_data WHERE Date BETWEEN ? AND ?"
        c.execute(query, (start_date, end_date))
        rows = c.fetchall()
        # write_dict_to_file(format_data(rows))
        return format_data(rows)
        # format_data(rows,start_date, end_date)
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def hydro(page_data=None):

    if request.method == 'POST':
         startDate = request.form.get("date-from")
    else:
        full_date = get_current_date_and_time()
        startDate = full_date[2]+"-"+full_date[1]+"-"+full_date[0]
        
     
    page_data={
        'temp': hydro_data.getTemp(),
        'humidity':hydro_data.getHumidity(),
        'light_status':hydro_data.getLightStatus(),
        'start_date':startDate,
        'end_date':startDate,
        'temp_humidity_data':get_data(startDate,startDate)
    }
    print(page_data)
    return render_template('index.html', page_data=page_data)

def hydro_webserver():
    app.run(host='0.0.0.0')

def hydro_electronics():
    try:
        while True:
            try: 
                current_time = get_current_date_and_time()
                climate_data = get_climate_data()
                hydro_data.setTemp(climate_data[0])
                hydro_data.setHumidity(climate_data[1])
                if hydro_data.writeClimateData(hydro_data.getLastTimeChecked(),(current_time[3],current_time[4])):
                    current_date_str = current_time[2]+ "-" +current_time[1]+ "-" +current_time[0]
                    current_time_str = current_time[3]+ ":" +current_time[4]
                    try:
                        write_data(current_date_str,current_time_str,climate_data[1],climate_data[0],hydro_data.getLightStatus())
                    except:
                        print("error writing data")

                    hydro_data.setLastTimeChecked(current_time[3],current_time[4])

                if hydro_data.switch_light_on(current_time[3]):
                    GPIO.output(LIGHT_RELAY_PIN, GPIO.LOW) 
                else:
                    GPIO.output(LIGHT_RELAY_PIN, GPIO.HIGH) 
            except:
                print("error is here")
            time.sleep(10)  # Wait for 10 minutes before checking again

    finally:
        GPIO.cleanup() # cleanup all GPIO  


if __name__ == "__main__":
    electronics_thread = threading.Thread(target=hydro_electronics)
    web_server_thread = threading.Thread(target=hydro_webserver)
    hydro_data = Hydro()
    print("created hydro object")
    start_time = get_current_date_and_time()
    print(start_time)
    hydro_data.setLastTimeChecked(start_time[3],start_time[4])
    print("about to start threads")
    electronics_thread.start()
    print("started electronics_thread")
    web_server_thread.start()

    

   