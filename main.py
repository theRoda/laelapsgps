import sdcard, os
from time import sleep
from machine import UART
from machine import SPI
from machine import Pin
import uping

connectWifi()
uping.ping('8.8.8.8')
spi = SPI(1, baudrate=20000000) # SPI interface on ESP32, SCK and MOSI pins are 14 and 15 respectively
cs = Pin(13) # CS pin is 13
sd = sdcard.SDCard(spi, cs)

vfs = os.VfsFat(sd)
os.mount(sd, "/sd")

with open("/sd/test.txt", "w") as f:
    f.write("Hello, World!")

with open("/sd/test.txt", "r") as f:
    print(f.read())

gps = UART(2, baudrate=9600)
print(gps)

while True:
    sleep(.1)
    line = gps.readline()
    if line is not None:
        try:
            decoded = line.decode().rstrip()
            chunks = decoded.split(',')
            if chunks[0] == '$GPGGA':
                print(decoded)
        except UnicodeError:
            pass

