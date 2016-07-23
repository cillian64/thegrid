import sys
import serial
ser = serial.Serial(sys.argv[1], 115200)
ser.write("\xCA\xFE\xBA\xBE\xDE\xAD\xBE\xEF")
