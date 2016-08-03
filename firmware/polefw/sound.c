
#include "ch.h"
#include "hal.h"
#include "sound.h"
#include <string.h>

#define TIMER_FREQ (16000000U)

static const GPTConfig gpt_cfg = {
    .frequency = TIMER_FREQ,
    .callback  = NULL,
    .cr2       = TIM_CR2_MMS_1,  /* MMS=010 -> TRGO on Update Event */
    .dier      = 0U,
};

static const DACConfig dac_cfg = {
    .init     = 0,
    .datamode = DAC_DHRM_12BIT_RIGHT,
};

static const uint16_t freq_lut[256] = {
    1999, 2008, 2018, 2028, 2038, 2047, 2057, 2067, 2077, 2087, 2097, 2107,
    2117, 2127, 2137, 2147, 2158, 2168, 2178, 2188, 2199, 2209, 2220, 2230,
    2241, 2251, 2262, 2272, 2283, 2294, 2304, 2315, 2326, 2337, 2348, 2359,
    2370, 2381, 2392, 2403, 2414, 2425, 2436, 2447, 2459, 2470, 2481, 2493,
    2504, 2516, 2527, 2539, 2550, 2562, 2574, 2586, 2597, 2609, 2621, 2633,
    2645, 2657, 2669, 2681, 2693, 2705, 2717, 2730, 2742, 2754, 2767, 2779,
    2792, 2804, 2817, 2829, 2842, 2855, 2867, 2880, 2893, 2906, 2919, 2932,
    2945, 2958, 2971, 2984, 2997, 3011, 3024, 3037, 3051, 3064, 3077, 3091,
    3105, 3118, 3132, 3146, 3159, 3173, 3187, 3201, 3215, 3229, 3243, 3257,
    3272, 3286, 3300, 3314, 3329, 3343, 3358, 3372, 3387, 3401, 3416, 3431,
    3446, 3461, 3475, 3490, 3505, 3521, 3536, 3551, 3566, 3581, 3597, 3612,
    3628, 3643, 3659, 3674, 3690, 3706, 3721, 3737, 3753, 3769, 3785, 3801,
    3817, 3834, 3850, 3866, 3883, 3899, 3915, 3932, 3949, 3965, 3982, 3999,
    4016, 4032, 4049, 4066, 4084, 4101, 4118, 4135, 4152, 4170, 4187, 4205,
    4222, 4240, 4258, 4276, 4293, 4311, 4329, 4347, 4365, 4384, 4402, 4420,
    4438, 4457, 4475, 4494, 4512, 4531, 4550, 4569, 4588, 4606, 4626, 4645,
    4664, 4683, 4702, 4722, 4741, 4761, 4780, 4800, 4819, 4839, 4859, 4879,
    4899, 4919, 4939, 4959, 4980, 5000, 5021, 5041, 5062, 5082, 5103, 5124,
    5145, 5166, 5187, 5208, 5229, 5250, 5271, 5293, 5314, 5336, 5358, 5379,
    5401, 5423, 5445, 5467, 5489, 5511, 5533, 5556, 5578, 5601, 5623, 5646,
    5669, 5691, 5714, 5737, 5760, 5784, 5807, 5830, 5854, 5877, 5901, 5924,
    5948, 5972, 5996
};

static const uint8_t sample_square[] = {
    0, 255
};
static const uint8_t sample_sine[] = {
    127, 133, 140, 146, 152, 158, 164, 170, 176, 182, 188, 193, 198, 203, 208,
    213, 218, 222, 226, 230, 234, 237, 240, 243, 245, 247, 249, 251, 252, 253,
    254, 254, 254, 254, 254, 253, 252, 250, 248, 246, 244, 241, 238, 235, 232,
    228, 224, 220, 215, 211, 206, 201, 196, 190, 185, 179, 173, 167, 161, 155,
    149, 143, 136, 130, 124, 118, 111, 105, 99, 93, 87, 81, 75, 69, 64, 58, 53,
    48, 43, 39, 34, 30, 26, 22, 19, 16, 13, 10, 8, 6, 4, 2, 1, 0, 0, 0, 0, 0,
    1, 2, 3, 5, 7, 9, 11, 14, 17, 20, 24, 28, 32, 36, 41, 46, 51, 56, 61, 66,
    72, 78, 84, 90, 96, 102, 108, 114, 121, 127
};
static const uint8_t sample_triangle[] = {
    128, 132, 136, 140, 144, 148, 152, 156, 160, 164, 168, 172, 176, 180, 184,
    188, 192, 196, 200, 204, 208, 212, 216, 220, 224, 228, 232, 236, 240, 244,
    248, 252, 255, 251, 247, 243, 239, 235, 231, 227, 223, 219, 215, 211, 207,
    203, 199, 195, 191, 187, 183, 179, 175, 171, 167, 163, 159, 155, 151, 147,
    143, 139, 135, 131, 127, 123, 119, 115, 111, 107, 103, 99, 95, 91, 87, 83,
    79, 75, 71, 67, 63, 59, 55, 51, 47, 43, 39, 35, 31, 27, 23, 19, 15, 11, 7,
    3, 0, 4, 8, 12, 16, 20, 24, 28, 32, 36, 40, 44, 48, 52, 56, 60, 64, 68, 72,
    76, 80, 84, 88, 92, 96, 100, 104, 108, 112, 116, 120, 124
};
static const uint8_t sample_noise[] = {
    0, 166, 110, 138, 88, 153, 109, 27, 176, 82, 200, 93, 120, 86, 128, 75,
    133, 153, 72, 193, 52, 0, 56, 112, 105, 131, 116, 105, 175, 119, 116, 146,
    172, 36, 144, 102, 127, 114, 212, 116, 152, 172, 196, 85, 231, 167, 138,
    106, 172, 153, 151, 63, 0, 143, 125, 144, 107, 147, 199, 102, 217, 159,
    119, 195, 106, 157, 72, 186, 60, 115, 107, 112, 83, 116, 0, 77, 115, 98,
    11, 107, 177, 113, 92, 136, 119, 159, 80, 59, 90, 43, 105, 48, 92, 133, 50,
    164, 63, 125, 119, 156, 217, 197, 132, 156, 136, 131, 50, 206, 159, 80, 57,
    128, 86, 255, 174, 142, 170, 136, 106, 146, 122, 121, 122, 204, 51, 115,
    172, 161, 86, 48, 120, 103, 60, 98, 152, 162, 157, 140, 99, 152, 114, 156,
    119, 125, 97, 124, 144, 95, 76, 174, 147, 178, 86, 86, 68, 52, 178, 151,
    145, 158, 113, 117, 18, 93, 176, 202, 185, 144, 234, 115, 126, 96, 52, 168,
    238, 114, 82, 194, 191, 114, 159, 95, 188, 98, 119, 164, 220, 49, 130, 121,
    216, 179, 178, 117, 163, 85, 94, 218, 45, 2, 154, 112, 91, 176, 130, 144,
    88, 93, 65, 235, 117, 109, 187, 100, 51, 142, 196, 206, 135, 194, 139, 88,
    48, 187, 107, 51, 108, 134, 83, 153, 85, 224, 163, 43, 206, 172, 163, 130,
    184, 174, 99, 119, 122, 113, 106, 211, 76, 156, 91, 144, 37, 94, 131, 139,
    255, 192
};
static const uint8_t sample_click[] = {
    255
};

typedef struct {
    const uint8_t* samples;
    const size_t len;
} sound_sample;

static const sound_sample sound_samples[] = {
    {NULL, 0},
    {sample_sine, sizeof(sample_sine)},
    {sample_square, sizeof(sample_square)},
    {sample_triangle, sizeof(sample_triangle)},
    {sample_noise, sizeof(sample_noise)},
    {sample_click, sizeof(sample_click)},
};

#define SOUND_SILENT    0
#define SOUND_SINE      1
#define SOUND_SQUARE    2
#define SOUND_TRIANGLE  3
#define SOUND_NOISE     4
#define SOUND_CLICK     5

#define SOUND_BUF_SIZE 512
static dacsample_t sound_buf[SOUND_BUF_SIZE];

static void sound_end_cb(DACDriver* dacp, const dacsample_t *buf, size_t n);

static const DACConversionGroup dac_grp_cfg = {
    .num_channels = 1U,
    .end_cb       = sound_end_cb,
    .error_cb     = NULL,
    .trigger      = DAC_TRG(0),
};


static void shuffle_noise(uint8_t mag);
static uint8_t current_sound = 0, current_freq = 0, current_mag = 0;

static binary_semaphore_t shuffle_thread_sem;
static THD_WORKING_AREA(shuffle_thread_wa, 128);
static THD_FUNCTION(shuffle_thread, arg) {
    (void)arg;
    while(true) {
        chBSemWait(&shuffle_thread_sem);
        shuffle_noise(current_mag);
    }
}

void sound_init() {
    dacStart(&DACD1, &dac_cfg);
    gptStart(&GPTD6, &gpt_cfg);
    chBSemObjectInit(&shuffle_thread_sem, FALSE);
    chThdCreateStatic(shuffle_thread_wa, sizeof(shuffle_thread_wa),
        NORMALPRIO, shuffle_thread, NULL);
}

void sound_set(uint8_t id, uint8_t freq, uint8_t mag) {
    (void)mag;
    if(current_sound == id && current_freq == freq && current_mag == mag) {
        /* do nothing if we're already playing this sound, to prevent glitches
         * due to restarting the sample
         */
        return;
    } else if(id == SOUND_SILENT) {
        /* go silent */
        dacStopConversion(&DACD1);
        gptStopTimer(&GPTD6);
    } else if(id == SOUND_NOISE) {
        /* randomly load the noise sound and run at a fixed frequency */
        dacStopConversion(&DACD1);
        gptStopTimer(&GPTD6);
        shuffle_noise(mag);
        gptStartContinuous(&GPTD6, 2048);
        dacStartConversion(&DACD1, &dac_grp_cfg, sound_buf, SOUND_BUF_SIZE);
    } else if(id == SOUND_CLICK) {
        /* blocking play a single 0.1ms click at the given volume */
        dacStopConversion(&DACD1);
        gptStopTimer(&GPTD6);
        dacPutChannelX(&DACD1, 0, 1028+mag);
        chThdSleepMicroseconds(100);
        dacPutChannelX(&DACD1, 0, 0);
    } else if(id < sizeof(sound_samples)/sizeof(sound_samples[0])) {
        /* load the samples into the buffer, scaling by mag, then play back
         * at appropriate frequency
         */
        dacStopConversion(&DACD1);
        gptStopTimer(&GPTD6);
        sound_sample sound = sound_samples[id];
        size_t i;
        for(i=0; i<sound.len && i<SOUND_BUF_SIZE; i++) {
            uint32_t samp = ((uint16_t)sound.samples[i] * (mag+1)) >> 8;
            sound_buf[i] = samp + 1028;
        }
        unsigned int freq_hz = freq_lut[freq];
        unsigned int interval = TIMER_FREQ / (freq_hz * sound.len);
        gptStartContinuous(&GPTD6, interval);
        dacStartConversion(&DACD1, &dac_grp_cfg, sound_buf, sound.len);
    } else {
        /* oops. just stop. */
        dacStopConversion(&DACD1);
        gptStopTimer(&GPTD6);
    }
    current_sound = id;
    current_freq = freq;
    current_mag = mag;
}

/* at the end of each SOUND_NOISE conversion, reshuffle the noise so it doesn't
 * sound periodic.
 */
static void sound_end_cb(DACDriver* dacp, const dacsample_t *buf, size_t n) {
    (void)dacp;
    (void)buf;
    (void)n;
    if(current_sound == SOUND_NOISE) {
        chSysLockFromISR();
        chBSemSignalI(&shuffle_thread_sem);
        chSysUnlockFromISR();
    }
}

uint8_t lfsr(void);
uint8_t lfsr() {
    static uint16_t s = 0xCAFE;
    uint8_t b = s & 1;
    s >>= 1;
    s ^= (-b) & 0xB400;
    return b;
}

/* randomly load sample_noise into sound_buf (scaled by mag), so that it
 * doesn't sound periodic when the same random noise is repeated over and over.
 */
static void shuffle_noise(uint8_t mag) {
    static uint32_t i, j=0;
    for(i=0; i<SOUND_BUF_SIZE; i++) {

        /* increment j while lfsr returns 1 */
        j++;
        while(lfsr()) {
            if(j++ >= sizeof(sample_noise)) {
                j = 0;
            }
        }

        /* copy into buffer from sample j */
        sound_buf[i] = (((uint16_t)sample_noise[j] * (mag+1)) >> 8) + 1028;
    }
}
