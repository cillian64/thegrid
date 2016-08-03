import time
import serial
import argparse
import struct

parser = argparse.ArgumentParser()
parser.add_argument("serial_port", help="path to serial port")
args = parser.parse_args()
ser = serial.Serial(args.serial_port, 115200)


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


def makeframe(grid):
    sync = b"\xFF"*6
    packets = b""
    for pole in grid:
        packets += struct.pack("6B", *pole)
    crc = struct.pack("H", checksum(packets))
    frame = sync + packets + crc
    return frame


def main():
    off = makeframe([(0, 0, 0, 0, 0, 0)]*49)
    red = makeframe([(1, 200, 200, 255, 0, 0)]*49)
    grn = makeframe([(1, 200, 200, 0, 255, 0)]*49)
    blu = makeframe([(1, 200, 200, 0, 0, 255)]*49)

    # Send a few frames to let the poles get in sync
    for _ in range(20):
        ser.write(off)
        time.sleep(0.1)

    # Flash red, green, blue
    for frame in (red, grn, blu):
        ser.write(frame)
        time.sleep(0.2)
        ser.write(off)
        time.sleep(0.2)


if __name__ == "__main__":
    main()
