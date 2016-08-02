import serial
import argparse
import struct
import time

parser = argparse.ArgumentParser(description="The.Grid Node Sounds")
parser.add_argument("serial_port", help="path to serial port")
parser.add_argument("--baud", type=int,
                    help="serial baud, default 115200", default=115200)
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
    sync = struct.pack("6B", 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF)
    packets = b""
    for pole in grid:
        packets += struct.pack("6B", *pole)
    crc = struct.pack("H", checksum(packets))
    frame = sync + packets + crc
    return frame


def main():
    sounds = [
        #(0, 0, 0, 0, 0, 0),
        #(1, 0, 100, 50, 0, 0),
        #(2, 0, 100, 50, 50, 0),
        #(4, 0, 100, 0, 50, 0),
        #(0, 0, 0, 0, 50, 50),
        #(5, 0, 255, 0, 0, 50),
        (4, 0, 255, 0, 0, 0),
        (0, 0, 0, 0, 0, 0),
    ]
    while True:
        for sound in sounds:
            grid = [sound] * 49
            frame = makeframe(grid)
            ser.write(frame)
            time.sleep(1/50)

if __name__ == "__main__":
    main()
