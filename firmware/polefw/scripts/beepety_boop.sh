#!/bin/bash

make

while true
do
	if arm-none-eabi-gdb --batch \
                      -return-child-result \
		              -ex 'target extended-remote /dev/cu.usbmodemD6CBAEC1' \
					  -ex 'monitor version' \
					  -ex 'monitor swdp_scan' \
					  -ex 'attach 1' \
					  -ex 'load' \
                      build/testfw.elf | grep Transfer
    then
        echo Programmed okay: sending magic
        afplay tada.mp3
        python3 send_magic.py /dev/tty.usbserial-A1001Nsc
        sleep 5
    else
        echo Fail!
        sleep 1
    fi
done

