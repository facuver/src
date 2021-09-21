from .cfg import configs
import wifi
import ntptime

print(configs)

# start the Access point and contect to wifi saved on config.json
wifi.do_create()
if configs["STA_essid"]:
    wifi.do_connect(configs["STA_essid"], configs["STA_password"])

# set the npt time host to google and set the time to the RTC
ntptime.host = "time.google.com"
ntptime.settime()
