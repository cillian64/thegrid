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

uint32_t prng_state;
const uint32_t m=214013, a=2531011, RAND_MAX=(1u<<31) - 1;
uint32_t prng(void);
uint32_t prng(void)
{
    /* Simple Linear congruential generator */
    prng_state = (prng_state * m + a) & RAND_MAX;
    return prng_state >> 16;
}

uint32_t randint(uint32_t max)
{
    /* Generate a random integer between 0 and max */
    return prng() * max / (1<<16);
}

static THD_WORKING_AREA(waThreadLEDs, 512);
static THD_FUNCTION(threadLEDs, arg) {
    (void)arg;
    chRegSetThreadName("LEDs");
    int r=0, g=0, b=0;
    while (true) {
        r=20 + randint(80);
        g=randint(20);
        b=0;
        if(g*4 > r)
            g=r/4; /* Don't let us go too green */
        if(r > g*10)
            r = g*10; /* Don't let us go too red */
        pwmEnableChannel(&PWMD1, 1, r);
        pwmEnableChannel(&PWMD1, 0, g);
        pwmEnableChannel(&PWMD1, 2, b);
        chThdSleepMilliseconds(80);
    }
}

static const GPTConfig gpt6cfg = {
  .frequency    = 1500000U,
  .callback     = NULL,
  .cr2          = TIM_CR2_MMS_1,    /* MMS = 010 = TRGO on Update Event.    */
  .dier         = 0U
};

int main(void) {

    halInit();
    chSysInit();

    pwmStart(&PWMD1, &pwmcfg);

    gptStart(&GPTD6, &gpt6cfg);

    gptStartContinuous(&GPTD6, 2U);

    chThdCreateStatic(waThreadLEDs, sizeof(waThreadLEDs),
                      NORMALPRIO, threadLEDs, NULL);

    while (true) {
    }
}
