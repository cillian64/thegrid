
#include <stdbool.h>
#include "ch.h"
#include "hal.h"
#include "frame.h"
#include "bus.h"
#include "power.h"

volatile Frame framebuf;

static bool frame_check_sync(void) {
    return (
        framebuf.sync[0] == CMD_SYNC &&
        framebuf.sync[1] == CMD_SYNC &&
        framebuf.sync[2] == CMD_SYNC &&
        framebuf.sync[3] == CMD_SYNC &&
        framebuf.sync[4] == CMD_SYNC &&
        framebuf.sync[5] == CMD_SYNC
    );
}

void frame_process() {
    if(!frame_check_sync())
        return;

    if(framebuf.packets[0].cmd_id == CMD_POWER) {
        power_set();
    } else {
        bus_tx();
    }
}
