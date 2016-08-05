#include <stdbool.h>
#include "ch.h"
#include "hal.h"
#include "bus.h"
#include "frame.h"

static void bus_rx(UARTDriver*, uint16_t);

extern binary_semaphore_t frame_thread_sem;

static const UARTConfig uart_cfg = {
    .txend1_cb = NULL,
    .txend2_cb = NULL,
    .rxend_cb  = NULL,
    .rxchar_cb = bus_rx,
    .rxerr_cb  = NULL,
    .speed     = 1000000,
    .cr1       = 0,
    .cr2       = 0,
    .cr3       = 0,
};

static void bus_rx(UARTDriver *uartp, uint16_t c)
{
    (void)uartp;
    static unsigned int framebuf_ctr = 0;
    static unsigned int sync_ctr = 0;
    static uint16_t last_c = 0;

    framebuf.raw[framebuf_ctr++] = c;

    if(last_c == CMD_SYNC && c == CMD_SYNC) {
        sync_ctr += 1;
        if(sync_ctr == 5) {
            framebuf.raw[0] = CMD_SYNC;
            framebuf.raw[1] = CMD_SYNC;
            framebuf.raw[2] = CMD_SYNC;
            framebuf.raw[3] = CMD_SYNC;
            framebuf.raw[4] = CMD_SYNC;
            framebuf.raw[5] = CMD_SYNC;
            framebuf_ctr = 6;
        }
    } else {
        sync_ctr = 0;
    }

    last_c = c;

    if(framebuf_ctr == sizeof(Frame)) {
        framebuf_ctr = 0;
        chSysLockFromISR();
        chBSemSignalI(&frame_thread_sem);
        chSysUnlockFromISR();
    }
}

void bus_init() {
    uartStart(&UARTD2, &uart_cfg);
}
