import serial
import time

ser = serial.Serial("/dev/ttyACM0", 115200)

while True:
    print("on")
    ser.write(bytearray([2, 255, 255, 255, 255, 255, 255, 255, 3]))
    time.sleep(1)

    print("off")
    ser.write(bytearray([2, 0, 0, 0, 0, 0, 0, 0, 3]))
    time.sleep(1)
