import serial
import struct
import sys
import time

ser = serial.Serial(sys.argv[1], 115200)


def main2():
    make_power_frame(0, 0)
    make_id_frame(6)
    make_power_frame(2, 6)
    make_id_frame(7*3)


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


def make_id_frame(new_id):
    sync = b"\xFF" * 6
    cmd = (0xFE, 0xFE, 0xFE, 0xFE, 0xFE, new_id & 0xFF)
    packets = b""
    for _ in range(49):
        packets += struct.pack("6B", *cmd)
    crc = struct.pack("H", checksum(packets))
    return sync + packets + crc


def make_power_frame(i, j):
    sync = b"\xFF" * 6
    cmd = b"\xFC"
    for row in range(7):
        rowbyte = 0
        for col in range(7):
            if row == (6-i) and col == j:
                rowbyte = 1 << col
        cmd += struct.pack("B", rowbyte)
    cmd += b"\x00" * 286
    crc = struct.pack("H", checksum(cmd))
    return sync + cmd + crc


def make_check_frame(new_id):
    sync = b"\xFF"*6
    packets = b""
    for pole_id in range(49):
        if pole_id == new_id:
            packets += struct.pack("6B", 1, 255, 255, 0, 255, 0)
        else:
            packets += struct.pack("6B", 2, 100, 255, 255, 0, 0)
    crc = struct.pack("H", checksum(packets))
    return sync + packets + crc


def main():
    for i in range(7):
        for j in range(7):
            new_id = i*7 + j
            print("Setting pole ({}, {}) to ID {}".format(i, j, new_id))
            ser.write(make_power_frame(i, j))
            time.sleep(0.3)
            for _ in range(10):
                ser.write(make_id_frame(new_id))
                time.sleep(0.3)
                ser.write(make_check_frame(new_id))
            time.sleep(0.5)


if __name__ == "__main__":
    main2()
