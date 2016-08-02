/*
 * The.Grid
 * Pole Firmware
 * Copyright 2016 Adam Greig, David Turner
 */

#include <string.h>
#include "ch.h"
#include "hal.h"
#include "leds.h"
#include "bus.h"
#include "sound.h"
#include "frame.h"
#include "flash.h"

binary_semaphore_t frame_thread_sem;
static THD_WORKING_AREA(frame_thread_wa, 1024);
static THD_FUNCTION(frame_thread, arg) {
    (void)arg;

    while(true) {
        chBSemWait(&frame_thread_sem);
        frame_process();
    }
}

int main(void)
{
    halInit();
    chSysInit();

    chBSemObjectInit(&frame_thread_sem, FALSE);

    bus_init();
    leds_init();
    sound_init();
    flash_init();

    chThdCreateStatic(frame_thread_wa, sizeof(frame_thread_wa),
        NORMALPRIO, frame_thread, NULL);

    while(true) {}
}
