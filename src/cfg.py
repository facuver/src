import ujson
import logger
import utime
from uos import stat

# default config if config.json dont exist
default = {
    "AP_password": "test1234",
    "AP_essid": "iSpindel_Repeater",
    "update_interval": "600",
    "API_KEY": "",
    "Channel_ID": 0,
    "STA_essid": "",
    "STA_password": "",
}
# default config if automation.json dont exist
automation_defaults = {
    "ligth": {"status": 0, "time_on": 0, "time_off": 0, "time": 0},
    "pump": 0,
    "humidity": 0,
    "temperature_target": 60,
    "soil_target": 0,
    "soil_humidity": 0,
    "water_reserve": 0,
    "temp": 0,
    "fans": {"status": 0, "duty": 0},
}

# load the configs.json file to configs
def read_configs() -> dict:
    try:
        with open("src/config.json", "r") as f:
            conf = ujson.load(f)
    except Exception as e:
        print("Error: ", e)
        return default

    return conf


# dump configs to configs.json
def update_configs(conf: dict) -> dict:
    with open("src/config.json", "w") as f:
        ujson.dump(conf, f)
    return conf


# read automation.json to automation
def read_automation():
    try:
        with open("src/automation.json", "r") as f:
            auto = ujson.load(f)
    except Exception as e:
        print("Error: ", e)
        return automation_defaults

    return auto


# dump automation to automation.json
def update_automation(auto):
    print(auto)
    with open("src/automation.json", "w") as f:
        ujson.dump(auto, f)
    return auto


# return the time in a human frendly format withe the ajusted timezone
def format_time(time_zone=-3):
    time = utime.localtime(ntptime.time() + (time_zone * 3600))
    time = "{:02d}-{:02d}-{} {:02d}:{:02d}:{:02d}".format(
        time[2], time[1], time[0], time[3], time[4], time[5]
    )
    return time


# if log file under 1MB log the msg with the time formated
def log(msg):
    if stat("log.txt")[6] < 1_000_000:
        try:
            with open("log.txt", "a") as f:

                f.write("[{}] {} \n".format(format_time(), msg))
        except Exception as e:
            print(e)
    else:
        print("log full")


configs = read_configs()
automation = read_automation()

log = logger.LoggerSimple(utime, "Runtime")

# default ip from AP
ip = "192.168.4.1"
