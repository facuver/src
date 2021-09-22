days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
months = [
    "Jan",
    "Feb",
    "Mar",
    "Apr",
    "May",
    "Jun",
    "Jul",
    "Aug",
    "Sep",
    "Oct",
    "Nov",
    "Dec",
]


class Time:
    def __init__(self, time=None, time_zone=-3):
        self._time = time
        self.time_zone = time_zone

    def time(self):
        return self._time.time()

    def sleep(self, n):
        return self._time.sleep(n)

    def localtime(self):
        t = self._time.localtime(self.time() + (self.time_zone * 3600))
        return (t[0], t[1], t[2], t[3], t[4], t[5], t[6], t[7])

    def dateTimeIso(self):
        t = self.localtime()
        return "%d-%02d-%02d %02d:%02d:%02d" % (t[0], t[1], t[2], t[3], t[4], t[5])

    def human(self):
        t = self.localtime()
        return "%s, %d %s %d %02d:%02d:%02d" % (
            days[t[6]],
            t[2],
            months[t[1] - 1],
            t[0],
            t[3],
            t[4],
            t[5],
        )

    def sleep_us(self, n):
        return self._time.sleep_us(n)
