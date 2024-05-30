import sdcard, os
from time import sleep
from machine import UART
# from machine import SPI
from machine import SoftSPI
from machine import Pin
import uping

connectWifi()
uping.ping('8.8.8.8')

# MISO GPIO13
# MOSI GPIO12
# SCK GPIO14
# CS GPIO27
# GND - GND on left, next to VIN
# VCC - VIN, on left
spi = SoftSPI(-1, miso=Pin(13), mosi=Pin(12), sck=Pin(14))
cs = Pin(27)
sd = sdcard.SDCard(spi, cs)

vfs = os.VfsFat(sd)
os.mount(sd, "/sd")

# GREEN - ESP32 RX2 -> NEO-6M TX2
# BLUE - ESP32 TX2 -> NEO-6M RX2
gps = UART(2, baudrate=9600)
print(gps)

while True:
    sleep(.1)
    line = gps.readline()
    if line is not None:
        try:
            decoded = line.decode('utf-16')
            with open("/sd/gps_sentences.txt", "a") as f:
                f.write(decoded)
            print(decoded)
            # chunks = decoded.split(',')
            # if chunks[0] == '$GPGGA':
            #    print(decoded)
        except UnicodeError:
            pass


