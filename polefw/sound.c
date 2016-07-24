
#include "ch.h"
#include "hal.h"
#include "sound.h"

static const GPTConfig gpt_cfg = {
    .frequency = 48000U,
    .callback  = NULL,
    .cr2       = TIM_CR2_MMS_1,  /* MMS=010 -> TRGO on Update Event */
    .dier      = 0U,
};

static const DACConfig dac_cfg = {
    .init     = 0,
    .datamode = DAC_DHRM_12BIT_RIGHT,
};

#define DAC_BUF_SIZE 2048
static dacsample_t dac_buf[DAC_BUF_SIZE];

static const DACConversionGroup dac_grp_cfg = {
    .num_channels = 1U,
    .end_cb       = NULL,
    .error_cb     = NULL,
    .trigger      = DAC_TRG(0),
};

void sound_init() {
    dacStart(&DACD1, &dac_cfg);
    gptStart(&GPTD6, &gpt_cfg);
}

void sound_set(uint8_t id, uint8_t freq, uint8_t mag) {
    (void)mag;
    if(id == 0) {
        dacStopConversion(&DACD1);
        gptStopTimer(&GPTD6);
    } else {
        dacStartConversion(&DACD1, &dac_grp_cfg, dac_buf, DAC_BUF_SIZE);
        gptStartContinuous(&GPTD6, freq);
    }
}
