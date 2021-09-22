from machine import Signal, Pin, ADC
from dht import DHT11
import utime
from .cfg import log


class Pump(Signal):
    pass


class Led(Signal):
    pass


class Fan(Signal):
    pass


class AirSensor(DHT11):
    def __init__(self, pin):
        DHT11.__init__(self, pin)

    def read(self):
        try:
            self.measure()
            return (self.temperature(), self.humidity())
        except Exception as e:
            print(e)

        return (-1, -1)


class SoilProbe:
    def __init__(self, pin, in_min=340, in_max=900):
        self.pin = pin
        self.adc = ADC(self.pin)
        self.adc.width(ADC.WIDTH_10BIT)
        self.adc.atten(ADC.ATTN_11DB)
        self.in_min = in_min
        self.in_max = in_max

    def read(self):
        return 100 - int(
            ((self.read_raw() - self.in_min) * 100) / (self.in_max - self.in_min)
        )

    def read_raw(self):
        return self.adc.read()


class PumpActutor:
    def __init__(self, sensor, pump, target):
        self.target = target
        self.sensor = sensor
        self.pump = pump

    def update(self):
        if self.sensor.read() < self.target:
            self.pump.on()
        else:
            self.pump.off()


class LedActuator:
    def __init__(self, led, time, time_on, time_off, last_on=0, last_off=0):
        self.led = led
        self.time = time
        self.time_on = time_on
        self.time_off = time_off
        self.last_off = last_off
        self.last_on = last_on

    def update(self):
        current_time = self.time.time()
        if self.led.value():
            if (current_time - self.last_on) >= self.time_on:
                self.led.off()
                log("LED OFF")
                self.last_off = current_time
        else:
            if (current_time - self.last_off) >= self.time_off:
                self.led.on()
                log("LED ON")
                self.last_on = current_time

    def off(self):
        self.led.off()
        self.last_off = self.time.time()

    def on(self):
        self.led.on()
        self.last_on = self.time.time()


class FanActuator:
    def __init__(self, fan, sensor, target):
        self.fan = fan
        self.sensor = sensor
        self.target = target

    def update(self):
        if self.sensor.read()[0] > self.target:
            self.fan.on()
        else:
            self.fan.off()
