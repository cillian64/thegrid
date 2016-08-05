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


def make_on_frame(sound, freq, mag, r, g, b):
    sync = b"\xFF"*6
    packets = b""
    for pole_id in range(49):
        packets += struct.pack("6B", sound, freq, mag, r, g, b)
    crc = struct.pack("H", checksum(packets))
    return sync + packets + crc


def make_power_frame(on):
    sync = b"\xFF" * 6
    if on:
        cmd = b"\xFC" + b"\xFF"*7
    else:
        cmd = b"\xFC" + b"\x00"*7
    cmd += b"\x00" * 286
    crc = struct.pack("H", checksum(cmd))
    return sync + cmd + crc


def main():
    ser.write(make_power_frame(True))

if __name__ == "__main__":
    main()
