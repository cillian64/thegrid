
#include <stdbool.h>
#include "ch.h"
#include "hal.h"
#include "frame.h"
#include "bus.h"
#include "power.h"

volatile Frame framebuf;

static bool packet_check_sync(void) {
    return (
        framebuf.sync[0] == CMD_SYNC &&
        framebuf.sync[1] == CMD_SYNC &&
        framebuf.sync[2] == CMD_SYNC &&
        framebuf.sync[3] == CMD_SYNC &&
        framebuf.sync[4] == CMD_SYNC &&
        framebuf.sync[5] == CMD_SYNC
    );
}

static bool packet_check_checksum(void) {
    size_t i, j;
    uint16_t checksum = 0xFFFF;
    for(i=0; i<sizeof(framebuf.packets); i++) {
        checksum ^= ((uint16_t)framebuf.raw[i+6]) << 8;
        for(j=0; j<8; j++) {
            if(checksum & 0x8000)
                checksum = (checksum << 1) ^ 0x1021;
            else
                checksum <<= 1;
        }
    }
    return checksum == framebuf.checksum;
}

void frame_process() {
    if(!packet_check_sync())
        return;

    if(!packet_check_checksum())
        return;

    if(framebuf.packets[0].cmd_id == CMD_POWER) {
        power_set();
    } else {
        bus_tx();
    }
}
