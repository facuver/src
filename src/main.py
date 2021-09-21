print("STARTTT")

import uasyncio as asyncio
from .lib.periferics import led, soil, pump, dht11, fan, get_status
import gc
from .lib import urequests as requests
from .web import app
import wifi
from .cfg import automation, log, configs, format_time,update_automation


def soil_update():
    # check soil read an update the pump
    if soil.read() < automation["soil_target"]:
        pump.on()
    else:
        pump.off()


def fan_update():
    # check air humiditiy and update the fan
    if dht11.read()[0] > automation["temperature_target"]:
        fan.on()
    else:
        fan.off()


async def every_second():
    """
    func that run every 3 seconds
    useful for have a finer controll on pump
    """
    while True:
        soil_update()
        gc.collect()
        await asyncio.sleep(3)


async def every_minute() -> None:
    # func that run every minute
    while True:
        led.update()
        fan_update()
        update_automation(automation)
        # async sleep one minute
        await asyncio.sleep(60)


async def check_connection():
    # check if sta interface is connected  not sure if necesary, esp sdk migth doit on its own
    while True:
        print("checking Connection")
        if not wifi.interface.isconnected():
            log("Reconnecting")
            wifi.do_connect(wifi.configs["STA_essid"], wifi.configs["STA_password"])
        await asyncio.sleep(300)


async def update_data():
    """
    send data to thingspeak api,
    format the data with the periferics status

    """
    while True:

        await asyncio.sleep(int(configs["Update_interval"]))
        print("update_data")
        status = get_status()
        data = {
            "write_api_key": configs["API_KEY"],
            "updates": [
                {
                    "created_at": format_time(0),
                    "field1": status["ligth"]["status"],
                    "field2": status["humidity"],
                    "field3": status["temp"],
                    "field4": status["soil_humidity"],
                    "field5": status["fans"],
                    "field6": status["pump"],
                }
            ],
        }
        url = "http://api.thingspeak.com/channels/{}/bulk_update.json".format(
            configs["Channel_ID"]
        )
        try:
            r = requests.post(
                url,
                json=data,
                headers={"Content-type": "application/json"},
            )
            print(r.text)
        except Exception as e:
            print(e)
            log("Fail to send data")


log("Starting Server")
main_task = asyncio.create_task(every_minute())
second_task = asyncio.create_task(every_second())
# update_task = asyncio.create_task(update_data())

check_connection = asyncio.create_task(check_connection())
app.run(host="0.0.0.0", port=80, debug=True)
