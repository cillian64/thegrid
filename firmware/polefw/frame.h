#ifndef FRAME_H
#define FRAME_H

#define CMD_SYNC        (0xFF)
#define CMD_SET_ID      (0xFE)
#define CMD_BOOTLOAD    (0xFD)
#define CMD_POWER       (0xFC)

typedef struct {
    union {
        struct {uint8_t sound_id, sound_freq, sound_mag, r, g, b; };
        struct {uint8_t cmd_id, payload[5]; };
    };
} __attribute__((packed)) Packet;

typedef struct {
    union {
        uint8_t raw[302];
        struct {
            uint8_t sync[6];
            Packet packets[49];
            uint16_t checksum;
        };
    };
} __attribute__((packed)) Frame;

extern volatile Frame framebuf;

void frame_process(void);
#endif
