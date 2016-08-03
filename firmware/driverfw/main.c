/*
 * The.Grid
 * Driver Firmware
 * Copyright 2016 Adam Greig, David Turner
 */

#include <string.h>
#include "ch.h"
#include "hal.h"
#include "usbcfg.h"
#include "frame.h"
#include "bus.h"
#include "power.h"

binary_semaphore_t frame_thread_sem;
static THD_WORKING_AREA(frame_thread_wa, 128);
static THD_FUNCTION(frame_thread, arg) {
    (void)arg;
    while(true) {
        chBSemWait(&frame_thread_sem);
        frame_process();
    }
}

static void usb_rx(uint8_t c)
{
    static int framebuf_ctr = 0;

    if(framebuf_ctr < 6) {
        /* Wait for sync packet */
        if(c != 0xFF) {
            framebuf_ctr = 0;
        } else {
            framebuf.sync[framebuf_ctr++] = c;
        }
    } else {
        /* Process new actual data */
        framebuf.raw[framebuf_ctr++] = c;
        if(framebuf_ctr == sizeof(framebuf)) {
            framebuf_ctr = 0;
            chSysLockFromISR();
            chBSemSignalI(&frame_thread_sem);
            chSysUnlockFromISR();
        }
    }
}

int main(void)
{
    halInit();
    chSysInit();

    chBSemObjectInit(&frame_thread_sem, false);

    bus_init();
    power_init();

    sduObjectInit(&SDU1);
    sduStart(&SDU1, &serusbcfg);

    usbDisconnectBus(serusbcfg.usbp);
    chThdSleepMilliseconds(1500);
    usbStart(serusbcfg.usbp, &usbcfg);
    usbConnectBus(serusbcfg.usbp);

    chThdCreateStatic(frame_thread_wa, sizeof(frame_thread_wa),
        NORMALPRIO, frame_thread, NULL);

    while(true) {
        usb_rx(streamGet(&SDU1));
    }
}
