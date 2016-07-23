#include <string.h>
#include "ch.h"
#include "hal.h"

static const uint8_t rxmagic[8] =
    {0xCA, 0xFE, 0xBA, 0xBE, 0xDE, 0xAD, 0xBE, 0xEF};
static volatile uint8_t rxbuf[8];
static volatile unsigned int rxbufctr = 0;
static volatile int rxstatus = 0;
static void uart_rx(UARTDriver *uartp, uint16_t c)
{
    (void)uartp;

    if(c == 0xCA) {
        rxbufctr = 0;
    }

    rxbuf[rxbufctr++] = (uint8_t)c;

    if(rxbufctr == 8) {
        if(memcmp(rxmagic, (uint8_t*)rxbuf, 8) == 0) {
            rxstatus = 1;
        } else {
            rxstatus = 2;
        }
        rxbufctr = 0;
    }
}

static const UARTConfig uart_cfg = {
    .txend1_cb = NULL,
    .txend2_cb = NULL,
    .rxend_cb  = NULL,
    .rxchar_cb = uart_rx,
    .rxerr_cb  = NULL,
    .speed     = 115200,
    .cr1       = 0,
    .cr2       = 0,
    .cr3       = 0,
};

static const DACConfig dac_cfg = {
    .init     = 0,
    .datamode = DAC_DHRM_12BIT_RIGHT,
};

static const GPTConfig gpt_cfg = {
    .frequency = 8000U,
    .callback  = NULL,
    .cr2       = TIM_CR2_MMS_1,  /* MMS=010 -> TRGO on Update Event */
    .dier      = 0U,
};

#define DAC_BUF_SIZE 2
static const dacsample_t dac_buf[DAC_BUF_SIZE] = {4095, 0};

static const DACConversionGroup dac_grp_cfg = {
    .num_channels = 1U,
    .end_cb       = NULL,
    .error_cb     = NULL,
    .trigger      = DAC_TRG(0),
};

static const PWMConfig pwm_cfg = {
    .frequency = 10000,
    .period    = 100,
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

static THD_WORKING_AREA(waThreadTest, 128);
static THD_FUNCTION(threadTest, arg) {
    (void) arg;
    while(true) {
        int i;
        if(rxstatus == 0) {
            for(i=0; i<3; i++) {
                pwmEnableChannel(&PWMD1, i, 100);
                pwmEnableChannel(&PWMD1, (i+1) % 3, 0);
                pwmEnableChannel(&PWMD1, (i+2) % 3, 0);

                if(i == 0)
                    gptStartContinuous(&GPTD6, 2U);
                else
                    gptStopTimer(&GPTD6);

                chThdSleepMilliseconds(333);
            }
        } else if(rxstatus == 1) {
            pwmEnableChannel(&PWMD1, LED_GRN, 100);
            pwmEnableChannel(&PWMD1, LED_RED, 0);
            pwmEnableChannel(&PWMD1, LED_BLU, 0);
            gptStartContinuous(&GPTD6, 3U);
            chThdSleepMilliseconds(500);
            pwmEnableChannel(&PWMD1, LED_GRN, 0);
            gptStopTimer(&GPTD6);
            chThdSleepMilliseconds(500);
        } else if(rxstatus == 2) {
            pwmEnableChannel(&PWMD1, LED_RED, 100);
            pwmEnableChannel(&PWMD1, LED_GRN, 0);
            pwmEnableChannel(&PWMD1, LED_BLU, 0);
            gptStartContinuous(&GPTD6, 5U);
            chThdSleepMilliseconds(500);
            pwmEnableChannel(&PWMD1, LED_RED, 0);
            gptStopTimer(&GPTD6);
            chThdSleepMilliseconds(500);
        }
    }
}

int main(void)
{
    halInit();
    chSysInit();

    uartStart(&UARTD2, &uart_cfg);
    dacStart(&DACD1, &dac_cfg);
    gptStart(&GPTD6, &gpt_cfg);
    pwmStart(&PWMD1, &pwm_cfg);
    dacStartConversion(&DACD1, &dac_grp_cfg, dac_buf, DAC_BUF_SIZE);

    chThdCreateStatic(waThreadTest, sizeof(waThreadTest),
                      NORMALPRIO, threadTest, NULL);

    while(true) {}
}
