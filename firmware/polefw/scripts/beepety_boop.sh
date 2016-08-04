#!/bin/bash

make

while true
do
	if arm-none-eabi-gdb --batch \
                      -return-child-result \
		              -ex 'target extended-remote /dev/ttyACM0' \
					  -ex 'monitor version' \
					  -ex 'monitor swdp_scan' \
					  -ex 'attach 1' \
					  -ex 'load' \
                      ../build/polefw.elf | grep Transfer
    then
        echo Programmed okay
        mplayer -really-quiet tada.mp3 2>/dev/null
        #python3 quicktest.py
        sleep 5
        echo Trying again...
    else
        echo Fail!
        sleep 1
    fi
done

