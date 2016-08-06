import serial
import struct
import sys
import time

ser = serial.Serial(sys.argv[1], 115200)


def checksum(data):
    crc = 0xFFFF
    for b in data:
        crc ^= b << 8
        for _ in range(8):
            if crc & 0x8000:
                crc = (crc << 1) ^ 0x1021
            else:
                crc <<= 1
            crc &= 0xFFFF
    return crc


def make_power_frame(i, j):
    sync = b"\xFF" * 6
    cmd = b"\xFC"
    for row in range(7):
        rowbyte = 0
        for col in range(7):
            if row == i and col == j:
                rowbyte = 1 << col
        cmd += struct.pack("B", rowbyte)
    cmd += b"\x00" * 286
    crc = struct.pack("H", checksum(cmd))
    return sync + cmd + crc


def main():
    while True:
        for i in range(7):
            for j in range(7):
                ser.write(make_power_frame(i, j))
                time.sleep(0.1)


if __name__ == "__main__":
    main()
