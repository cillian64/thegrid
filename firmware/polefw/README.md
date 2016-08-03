# Pole Firmware

Firmware for the pole PCBs.
Receive data over the differential serial bus, work out what's our data, and 
update the LED drivers and beeper appropriately.

## ChibiOS Bug
You'll need to apply this patch to your ChibiOS.

```
diff --git a/os/hal/ports/STM32/LLD/DACv1/dac_lld.c b/os/hal/ports/STM32/LLD/DACv1/dac_lld.c
index 3cea46d..2af4bba 100644
--- a/os/hal/ports/STM32/LLD/DACv1/dac_lld.c
+++ b/os/hal/ports/STM32/LLD/DACv1/dac_lld.c
@@ -284,9 +284,13 @@ void dac_lld_stop(DACDriver *dacp) {
 
 #if STM32_DAC_USE_DAC1_CH1
     if (&DACD1 == dacp) {
+#if STM32_DAC_USE_DAC1_CH2
       if ((dacp->params->dac->CR & DAC_CR_EN2) == 0U) {
         rccDisableDAC1(false);
       }
+#else
+      rccDisableDAC1(false);
+#endif
     }
 #endif
 
@@ -337,9 +341,11 @@ void dac_lld_put_channel(DACDriver *dacp,
     if (channel == 0U) {
       dacp->params->dac->DHR12R1 = (uint32_t)sample;
     }
+#if STM32_DAC_USE_DAC1_CH2
     else {
       dacp->params->dac->DHR12R2 = (uint32_t)sample;
     }
+#endif
     break;
   case DAC_DHRM_12BIT_LEFT:
 #if STM32_DAC_DUAL_MODE
@@ -348,9 +354,11 @@ void dac_lld_put_channel(DACDriver *dacp,
     if (channel == 0U) {
       dacp->params->dac->DHR12L1 = (uint32_t)sample;
     }
+#if STM32_DAC_USE_DAC1_CH2
     else {
       dacp->params->dac->DHR12L2 = (uint32_t)sample;
     }
+#endif
     break;
   case DAC_DHRM_8BIT_RIGHT:
 #if STM32_DAC_DUAL_MODE
@@ -359,9 +367,11 @@ void dac_lld_put_channel(DACDriver *dacp,
     if (channel == 0U) {
       dacp->params->dac->DHR8R1  = (uint32_t)sample;
     }
+#if STM32_DAC_USE_DAC1_CH2
     else {
       dacp->params->dac->DHR8R2  = (uint32_t)sample;
     }
+#endif
     break;
   default:
     osalDbgAssert(false, "unexpected DAC mode");
```
