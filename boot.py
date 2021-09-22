import ntptime, wifi, ujson, os, io
from machine import RTC

essid = ""
password = ""


try:
    with open("wifi.json", "r") as f:
        conf = ujson.load(f)
        essid = conf["essid"]
        password = conf["password"]

    if wifi.do_connect(essid, password):
        ntptime.host = "time.google.com"
        ntptime.settime()

    else:
        print("cant Connect")
        wifi.do_create()

except Exception as e:
    print("Error: ", e)
    wifi.do_create()
