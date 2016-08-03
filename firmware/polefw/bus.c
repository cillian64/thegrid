
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
    .speed     = 115200,
    .cr1       = 0,
    .cr2       = 0,
    .cr3       = 0,
};

static void bus_rx(UARTDriver *uartp, uint16_t c)
{
    (void)uartp;
    static unsigned int framebuf_ctr = 0;

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

void bus_init() {
    uartStart(&UARTD2, &uart_cfg);
}
