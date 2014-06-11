import time
import os

# File format:
# First line is a title
# Subsequent lines are
# description until a blank line:
#
# @OOOOOO
# # a comment
# O@OOOOO
# 100

f = open("wave.txt", 'r')

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

for block in blocks:
    for line in block[0:7]:
        print(line)
    time.sleep(float(block[7])/1000)
    print("\033[7A\r", end='')

print("\033[7B\r")

