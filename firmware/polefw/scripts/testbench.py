import serial
import colorsys
import argparse
import struct

parser = argparse.ArgumentParser(description="The.Grid Node Testbench")
parser.add_argument("serial_port", help="path to serial port")
parser.add_argument("--baud", type=int,
                    help="serial baud, default 115200", default=115200)
parser.add_argument("--set-id", type=int, help="set pole ID")
args = parser.parse_args()

ser = serial.Serial(args.serial_port, 115200)

grid = [(0, 0, 0, 0, 0, 0)] * 49


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


def makeframe():
    sync = struct.pack("6B", 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF)
    packets = b""
    for pole in grid:
        packets += struct.pack("6B", *pole)
    crc = struct.pack("H", checksum(packets))
    frame = sync + packets + crc
    return frame


def main():
    global grid
    if args.set_id is not None:
        print("Setting ID to", args.set_id)
        cmd = (0xFE, 0xFE, 0xFE, 0xFE, 0xFE, args.set_id & 0xFF)
        packets = b""
        for _ in range(49):
            packets += struct.pack("6B", *cmd)
        sync = struct.pack("6B", 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF)
        crc = struct.pack("H", checksum(packets))
        for _ in range(30):
            ser.write(sync + packets + crc)

    h = [hh/49 for hh in range(49)]
    f = 80
    while True:
        rgbs = [colorsys.hsv_to_rgb(hh, 1, 1) for hh in h]
        grid = [(4, int(f), 255, int(r*255), int(g*255), int(b*255))
                for (r, g, b) in rgbs]
        h = [0 if hh >= 1 else hh + 0.005 for hh in h]
        if f > 255:
            f = 100
        frame = makeframe()
        ser.write(frame)

if __name__ == "__main__":
    main()
