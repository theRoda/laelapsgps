#import sdcard
from time import sleep
from machine import UART

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
