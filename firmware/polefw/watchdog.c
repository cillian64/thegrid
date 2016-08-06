#include <stdbool.h>
#include "ch.h"
#include "hal.h"
#include "wdg.h"
#include "watchdog.h"

static const WDGConfig wdg_cfg = {
    .pr = STM32_IWDG_PR_256,
    .rlr = STM32_IWDG_RL(100),
    .winr = STM32_IWDG_WIN_DISABLED
};

void watchdog_start() {
    wdgStart(&WDGD1, &wdg_cfg);
}

void watchdog_reset() {
    wdgReset(&WDGD1);
}

void watchdog_stop() {
    wdgStop(&WDGD1);
}
