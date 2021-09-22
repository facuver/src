from .lib.microdot_asyncio import Microdot, send_file
from wifi import interface, get_scans

app = Microdot()

# index
@app.get("/")
async def index(request):
    return send_file("src/public/index.html")


# serve the files in public
@app.get("/public/<fn>")
async def get_public(request, fn):
    return send_file("src/public/{}".format(fn))


# return the ifconfig data
@app.get("/api/ifconfig")
async def ifconfig(request):
    return {"status": list(interface.ifconfig())}


# scans and return the aviable networks BLOCKING!!   takes a couple of seconds
@app.get("/api/scans")
async def scan(request):
    return {"net": get_scans()}


# return the log file
@app.get("/api/log")
async def log(request):
    return send_file("/log.txt")


# clear the log file
@app.get("/api/clear_log")
async def clear_log(request):
    with open("/log.txt", "w") as f:
        f.write("")
    return "Log Cleared"


# connect to the network sended from the request and reboot to reconnect
@app.post("/api/connect")
async def post_connect(request):
    net = request.json
    print(net)
    configs["STA_essid"] = net["essid"]
    configs["STA_password"] = net["password"]
    update_configs(configs)
    from machine import reset

    reset()


# return the status of periferics
@app.get("/api/home")
async def home(request):
    return get_status()


# stat the webrepl for debuggin, and OTA updates, may take controll of the program if wanted
@app.get("/api/start_webrepl")
async def start_webrepl(request):
    import webrepl

    webrepl.start(password="indoor")
    return "ws://192.168.0.100:8266"


# tuurn off the led useful for restart the time enlapsed
@app.get("/api/led_off")
async def led_off(request):
    led.off()
    return "OK"


# turn on the led usefull for restat the time enlapsed
@app.get("/api/led_on")
async def led_off(request):
    led.on()
    return "OK"


# update the automation file with the values from web
@app.post("/api/update_automation")
async def update_auto(request):
    res = request.json
    print(res)
    automation["ligth"]["time_on"] = int(res["ligth"]["time_on"]) * 60
    automation["ligth"]["time_off"] = int(res["ligth"]["time_off"]) * 60
    automation["soil_target"] = int(res["soil_target"])
    automation["temperature_target"] = int(res["temperature_target"])
    update_automation(automation)
    return "OK"
