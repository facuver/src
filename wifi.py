import utime as time
import network

interface = network.WLAN(network.STA_IF)
ap = network.WLAN(network.AP_IF)  # create access-point interface
ap.config(
    essid="INDOOR_ESP", password="indoor_esp"
)  # set the ESSID of the access point


def do_connect(ssid, pwd):
    print("Connecting")
    if not ssid:
        print("Disconnecting")
        interface.active(False)
        return False

    interface.active(True)
    interface.config(dhcp_hostname="indoor")
    interface.connect(ssid, pwd)

    for _ in range(15):
        if interface.isconnected():  # check if the station is connected to an AP
            print("\nnetwork config:", interface.ifconfig())
            print("Connect to: http://indoor.local")
            return True
        print(".", end="")
        time.sleep(1)
    print(" Connect attempt timed out\n")

    interface.active(False)

    return False


def do_create():
    ap.active(True)  # activate the interface


def get_scans():
    interface.active(True)
    scans = interface.scan()
    scans = [i[0].decode("utf-8") for i in scans]
    return scans
