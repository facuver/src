from machine import Pin
from . import periferics
import utime as time

led = periferics.Led(Pin(2, Pin.OUT))
ledActuactor = periferics.LedActuator(led, time, time_on=1, time_off=1)

pump = periferics.Pump(Pin(4, Pin.OUT))
soilProbe = periferics.SoilProbe(Pin(33))
pumpActuator = periferics.PumpActutor(soilProbe, pump, target=40)

fan = periferics.Fan(Pin(5, Pin.OUT))
airSensor = periferics.AirSensor(Pin(3))
fanActuator = periferics.FanActuator(fan, airSensor, target=25)
