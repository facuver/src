import ntptime, env, wifi, ujson

essid = ""
password = ""
try:
    with open("src/config.json", "r") as f:
        conf = ujson.load(f)
        essid = conf["STA_essid"]
        password = conf["STA_password"]
        print(essid, password)
except Exception as e:
    print("Error: ", e)


if wifi.do_connect(essid, password):
    ntptime.settime()
else:
    print("cant Connect")
    wifi.do_create()
