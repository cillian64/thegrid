
#include "ch.h"
#include "hal.h"
#include "leds.h"

static const PWMConfig pwm_cfg = {
    .frequency = 32000,
    .period    = 255,
    .callback  = NULL,
    .cr2       = 0,
    .dier      = 0,
    .channels  = {
        {
            .mode     = PWM_OUTPUT_ACTIVE_HIGH,
            .callback = NULL,
        },
        {
            .mode     = PWM_OUTPUT_ACTIVE_HIGH,
            .callback = NULL,
        },
        {
            .mode     = PWM_OUTPUT_ACTIVE_HIGH,
            .callback = NULL,
        },
        {
            .mode     = PWM_OUTPUT_DISABLED,
            .callback = NULL,
        },
    },
};

void leds_init() {
    pwmStart(&PWMD1, &pwm_cfg);
}

void leds_set(uint8_t r, uint8_t g, uint8_t b) {
    pwmEnableChannel(&PWMD1, LED_RED, r);
    pwmEnableChannel(&PWMD1, LED_GRN, g);
    pwmEnableChannel(&PWMD1, LED_BLU, b);
}
