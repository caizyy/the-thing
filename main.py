import machine
from wifihelper import get_signal_strength
import utime
import network
import socket
import gc
light = machine.Pin(1, machine.Pin.OUT)
led = machine.Pin("LED", machine.Pin.OUT)
led.value(0)
# Connecting to Wi-Fi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
networks = wlan.scan()
networks = sorted(networks, key=get_signal_strength)
for network in networks:
    ssid = network[0].decode()
    strength = network[3]
    if ssid == "": # skip if no name
        continue
    print(": 📶", ssid, "\n🎯", strength)
gc.collect()
wlan.connect("wifi", "password")
iteration = 0
while not wlan.isconnected():
    utime.sleep(0.5)
    led.value(0)
    utime.sleep(0.5)
    led.value(1)
    iteration += 1
    print("🔄📶")
    if iteration > 15:
        machine.reset()
# Wi-Fi connection is established
print("📶", wlan.isconnected())
led.value(1)
def timeoutDetect(c):
    if not c:
        print("!⌛️")#timeout
        work()
def work():
    while wlan.isconnected():
        iscomplete = False
        try:
            addr = socket.getaddrinfo("192.168.1.22", 3333)[0][-1]
            s = socket.socket()
            s.settimeout(10)  # Set the timeout to 10 seconds
            s.connect(addr)
            s.sendall(b"GET / HTTP/1.0\r\n\r\n")
            response = s.recv(4096)
            s.close()
            iscomplete = True
            value = response.decode().split("\r\n")[-1]
            print(value)
            light.value(int(value))
            print("💾: ", gc.mem_alloc(), "bytes")
        except OSError as e:
            print("⚠: ", e)
            timeoutDetect(iscomplete)

        gc.collect()

work()
# When wlan is no longer connected
machine.reset()


