
#include "ch.h"
#include "hal.h"
#include "bus.h"
#include "frame.h"

extern binary_semaphore_t frame_thread_sem;
static volatile unsigned int framebuf_ctr = 0;

static const UARTConfig uart_cfg = {
    .txend1_cb = NULL,
    .txend2_cb = NULL,
    .rxend_cb  = NULL,
    .rxchar_cb = NULL,
    .rxerr_cb  = NULL,
    .speed     = 115200,
    .cr1       = 0,
    .cr2       = 0,
    .cr3       = 0,
};

void bus_init() {
    uartStart(&UARTD2, &uart_cfg);
}

void bus_tx() {
    uartStartSend(&UARTD2, sizeof(Frame), &framebuf.raw);
}
