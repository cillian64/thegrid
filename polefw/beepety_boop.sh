#!/bin/bash

while true
do
    clear
	if arm-none-eabi-gdb --batch \
                      -return-child-result \
		              -ex 'target extended-remote /dev/ttyACM0' \
					  -ex 'monitor version' \
					  -ex 'monitor swdp_scan' \
					  -ex 'attach 1' \
					  -ex 'load' \
                      -ex 'compare-sections' build/polefw
    then
        echo Success!
        afplay tada.mp3
        sleep 5
    else
        echo Fail!
        sleep 1
    fi
done

