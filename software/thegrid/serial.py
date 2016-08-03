import asyncio
import struct
import serial_asyncio

transport = None


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


def frame_from_array(poles):
    sync = b"\xFF\xFF\xFF\xFF\xFF\xFF"
    packets = struct.pack("294B", *poles[:, :, [3, 4, 5, 0, 1, 2]].flat)
    crc = struct.pack("H", checksum(packets))
    return sync + packets + crc


@asyncio.coroutine
def open(port):
    global transport
    loop = asyncio.get_event_loop()
    reader = asyncio.StreamReader()
    proto = asyncio.StreamReaderProtocol(reader)
    transport, _ = yield from serial_asyncio.create_serial_connection(
        loop, lambda: proto, url=port, baudrate=115200)
    return transport


def write(poles):
    if transport is not None:
        frame = frame_from_array(poles)
        transport.write(frame)
