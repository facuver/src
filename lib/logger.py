import re
import io
import utime


class LoggerSimple:
    def __init__(self, time, prefix="", time_zone=-3):
        self.time = time
        self.prefix = prefix
        self.time_zone = time_zone

    def formated_time(self):
        t = self.time.localtime(self.time.time() + 3600 * self.time_zone)
        return "%d-%02d-%02d %02d:%02d:%02d" % (t[0], t[1], t[2], t[3], t[4], t[5])

    def append(self, pref):
        self.prefix = f"{self.prefix} {pref}"

    def __call__(self, msg):
        print(f"[{self.formated_time()}][{self.prefix}] {msg}")
