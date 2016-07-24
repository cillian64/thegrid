
#include <stdbool.h>
#include "ch.h"
#include "hal.h"
#include "frame.h"
#include "leds.h"
#include "sound.h"
#include "flash.h"

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

static void packet_set_node_id(Packet* pkt) {
    if(pkt->cmd_id == CMD_SET_ID &&
       pkt->payload[0] == CMD_SET_ID &&
       pkt->payload[1] == CMD_SET_ID &&
       pkt->payload[2] == CMD_SET_ID &&
       pkt->payload[3] == CMD_SET_ID) {
        flash_set_node_id(pkt->payload[4]);
    }
}

/* Placeholder */
static void bootloader_start(void) {}

static void packet_bootload(Packet* pkt) {
    if(pkt->cmd_id == CMD_BOOTLOAD &&
       pkt->payload[0] == CMD_BOOTLOAD &&
       pkt->payload[1] == CMD_BOOTLOAD &&
       pkt->payload[2] == CMD_BOOTLOAD &&
       pkt->payload[3] == CMD_BOOTLOAD &&
       pkt->payload[4] == CMD_BOOTLOAD) {
        bootloader_start();
    }
}

void frame_process() {
    if(!packet_check_sync())
        return;

    if(!packet_check_checksum())
        return;

    Packet pkt = framebuf.packets[node_id];
    switch(pkt.cmd_id) {
        case CMD_SYNC:
            return;
        case CMD_SET_ID:
            packet_set_node_id(&pkt);
            break;
        case CMD_BOOTLOAD:
            packet_bootload(&pkt);
            break;
        default:
            leds_set(pkt.r, pkt.g, pkt.b);
            sound_set(pkt.sound_id, pkt.sound_freq, pkt.sound_mag);
    }
}
