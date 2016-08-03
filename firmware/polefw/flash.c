
#include "ch.h"
#include "hal.h"
#include "flash.h"

#define FLASH_NODE_ID (0x08007C00);

uint8_t node_id;

void flash_init() {
    uint16_t* node_id_ptr = (uint16_t*)FLASH_NODE_ID;
    node_id = (uint8_t)(*node_id_ptr);
    if(node_id > 48) {
        node_id = 0;
    }
}

void flash_set_node_id(uint8_t id) {
    /* Wait for flash to be ready */
    while(FLASH->SR & FLASH_SR_BSY);

    /* Unlock the flash */
    FLASH->KEYR = FLASH_KEY1;
    FLASH->KEYR = FLASH_KEY2;

    /* Erase the flash page */
    FLASH->CR |= FLASH_CR_PER;
    FLASH->AR  = (uint16_t)FLASH_NODE_ID;
    FLASH->CR |= FLASH_CR_STRT;

    /* Wait for flash to be ready */
    while(FLASH->SR & FLASH_SR_BSY);

    /* Check erase completed then clear EOP bit by writing it */
    while(!(FLASH->SR & FLASH_SR_EOP));
    FLASH->SR |= FLASH_SR_EOP;
    FLASH->CR &= ~FLASH_CR_PER;

    /* Write flash */
    FLASH->CR |= FLASH_CR_PG;
    volatile uint16_t* node_id_ptr = (uint16_t*)FLASH_NODE_ID;
    *node_id_ptr = (uint16_t)id;

    /* Wait for write completion */
    while(FLASH->SR & FLASH_SR_BSY);

    /* Check write completed then clear bit */
    while(!(FLASH->SR & FLASH_SR_EOP));
    FLASH->SR |= FLASH_SR_EOP;
    FLASH->CR &= ~FLASH_CR_PG;

    /* Re-lock the flash */
    FLASH->CR |= FLASH_CR_LOCK;

    /* Re-read the new node ID */
    flash_init();
}
