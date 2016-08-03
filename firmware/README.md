# The·Grid Firmware

Firmware for the bus driver and the pole PCBs. Both are ChibiOS projects
running on STM32F0 microcontrollers.

To compile, you'll first need to apply a patch to the ChibiOS submodule, 
because current 3.0 master has a bug when using the single-channel DAC on an F0 
as it doesn't define various second-channel related stuff. To apply the patch:

```
git submodule update --init
cd ChibiOS/
cp ../chibios_dac.patch .
git apply chibios_dac.patch
```
