import machine
Timer = machine.Timer
import utime
import network
import urequests
import gc #import garbage collector

led = machine.Pin("LED", machine.Pin.OUT)  # assume the led has not been forcibly removed from the 
led.value(0)

# Connecting to Wi-Fi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect("your-wifi-network", "the-password")

# Waiting for the Wi-Fi connection to establish
iteration = 0
while not wlan.isconnected():
    print(wlan.isconnected())
    utime.sleep(0.5)
    led.value(0)
    utime.sleep(0.5)
    led.value(1)
    iteration += 1
    print("Connecting to wifi")
    if iteration > 20:
        machine.reset()

# Wi-Fi connection is established
print("Wi-Fi connected:", wlan.isconnected())
if wlan.isconnected():
    led.value(1)
def timeoutDetect(c):
    if c:
        return
    else:
        print("Device reset...")
        machine.reset()
while wlan.isconnected():
    iscomplete = False
    tim = Timer(period=10000, mode=Timer.ONE_SHOT, callback=lambda t:timeoutDetect(iscomplete))
    r = urequests.request("GET", "http://192.168.1.66/?temp" + str(gc.mem_alloc()))
    if r.text == "on":
        led.value(1)
    else:
        led.value(0)
    iscomplete = True
    print(r.status_code)
    print("Memory in use: ", gc.mem_alloc(), "bytes")
    r.close()
    gc.collect()
#when wlan is no longer connected
machine.reset()

