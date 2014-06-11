#!/usr/bin/python3

import time
import os
import sys

# File format:
# First line is a title
# Subsequent lines are
# description until a blank line:
#
# @OOOOOO
# # a comment
# O@OOOOO
# 100

if len(sys.argv) != 2:
    print("Sort out your arguments.")
    print("I want one argument, a filename to run. i.e:")
    print(sys.argv[0]+" patternfile.txt")
    exit()

try:
    f = open(sys.argv[1], 'r')
except FileNotFoundError:
    print("File `"+sys.argv[1]+"' doesn't seem to exist...")
    exit()

def fussyreadline(f):
    line = f.readline()
    if line == '':
        return ''
    line = line.rstrip()
    if line == '' or line[0] == '#':
        return fussyreadline(f)
    else:
        return line

title = f.readline().rstrip()
description = ""
line = f.readline().rstrip()
while(line != ''):
    description = description + line + " "
    line = f.readline().rstrip()

line = fussyreadline(f)
blocks = []
while(line != ''):
    block = []
    for _ in range(0, 8):
        block.append(line)
        line = fussyreadline(f).rstrip()
    blocks.append(block)

# dipslay time:
print("Title: "+title)
print("Description: "+description)
print("")

try:
    while True:
        for i,block in enumerate(blocks):
            for line in block[0:7]:
                print(line)
            framecount = str(len(blocks))
            frameno = str(i+1).zfill(len(framecount))
            print("Frame "+frameno+"/"+framecount)
            time.sleep(float(block[7])/1000)
            print("\033[8A\r", end='')
except KeyboardInterrupt:
    print("\033[8B\r")  # make sure our cursor isn't left in an odd place
    pass

