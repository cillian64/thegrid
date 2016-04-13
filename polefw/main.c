#include "ch.h"
#include "hal.h"

static PWMConfig pwmcfg = {
    10000,
    100,
    NULL,
    {
        {PWM_OUTPUT_ACTIVE_HIGH, NULL},
        {PWM_OUTPUT_ACTIVE_HIGH, NULL},
        {PWM_OUTPUT_ACTIVE_HIGH, NULL},
        {PWM_OUTPUT_DISABLED, NULL},
    },
    0,
    0
};

static THD_WORKING_AREA(waThreadLEDs, 512);
static THD_FUNCTION(threadLEDs, arg) {
    (void)arg;
    chRegSetThreadName("LEDs");
    while (true) {
        int ch;
        for(ch=0; ch<3; ch++) {
            int duty;
            for(duty=0; duty<100; duty++) {
                pwmEnableChannel(&PWMD1, ch, duty);
                chThdSleepMilliseconds(10);
            }
            for(duty=100; duty>0; duty--) {
                pwmEnableChannel(&PWMD1, ch, duty);
                chThdSleepMilliseconds(10);
            }
        }
    }
}

int main(void) {

    halInit();
    chSysInit();

    pwmStart(&PWMD1, &pwmcfg);

    chThdCreateStatic(waThreadLEDs, sizeof(waThreadLEDs),
                      NORMALPRIO, threadLEDs, NULL);

    while (true) {
    }
}
