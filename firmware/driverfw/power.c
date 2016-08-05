#include "ch.h"
#include "hal.h"
#include "power.h"
#include "frame.h"

static const SPIConfig spicfg = {
    NULL,
    GPIOA,
    GPIOA_NSS,
    SPI_CR1_BR_1 | SPI_CR1_BR_2,
    SPI_CR2_DS_2 | SPI_CR2_DS_1 | SPI_CR2_DS_0,
};

void power_init() {
    spiStart(&SPID1, &spicfg);
}

void power_set() {
    spiSelect(&SPID1);
    spiSend(&SPID1, 7, framebuf.raw + 7);
    spiUnselect(&SPID1);
}
