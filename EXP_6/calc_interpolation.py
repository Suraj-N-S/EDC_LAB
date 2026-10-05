import numpy as np

# Let's inspect the interpolation for Unity Gain:
# Midband reference: Gain_mid = 0 dB (|Av| = 1.000 V/V).
# Target -3 dB level: Gain_3dB = -3.00 dB (|Av| = 0.7071 V/V).

# 1. Low-frequency roll-off:
# Between f = 10 Hz (Gain = -2.62 dB, |Av| = 0.740) and f = 50 Hz (Gain = -7.13 dB, |Av| = 0.440):
# Linear interpolation in log10(f):
# (Gain - G1) / (G2 - G1) = (log10(f) - log10(f1)) / (log10(f2) - log10(f1))
f1, G1 = 10.0, -2.62
f2, G2 = 50.0, -7.13
G_target = -3.00
log_f = np.log10(f1) + (G_target - G1) / (G2 - G1) * (np.log10(f2) - np.log10(f1))
f_3db_low_u = 10**log_f
print(f"Unity Gain: Low-frequency -3 dB corner (log-f interp between 10 Hz and 50 Hz): {f_3db_low_u:.2f} Hz")

# Linear interpolation in f directly:
f_lin = f1 + (G_target - G1) / (G2 - G1) * (f2 - f1)
print(f"Unity Gain: Low-frequency -3 dB corner (linear f interp): {f_lin:.2f} Hz")

# Theoretical low-frequency corner:
# fc = 1 / (2 * pi * 18k * 1u) = 8.84 Hz
# Notice 10 Hz is at -2.62 dB, which is very close to -3 dB (just 0.38 dB away).
# If measured -2.62 dB is at 10 Hz, the actual corner is approximately ~10.4 Hz (by log-f interpolation) or 10 Hz!

# 2. Upper roll-off (from 100 Hz / 200 Hz down towards 500 Hz):
f1, G1 = 200.0, -1.11
f2, G2 = 500.0, -6.20
log_f_high = np.log10(f1) + (G_target - G1) / (G2 - G1) * (np.log10(f2) - np.log10(f1))
f_3db_high_u = 10**log_f_high
print(f"Unity Gain: Upper -3 dB corner (between 200 Hz and 500 Hz): {f_3db_high_u:.2f} Hz")

# Now for Gain of 10:
# Midband reference:
# At 50 Hz: |Av| = 8.20 V/V (+18.28 dB)
# At 500 Hz: |Av| = 7.70 V/V (+17.73 dB)
# At 700 Hz: |Av| = 8.00 V/V (+18.06 dB)
# Nominal midband gain = ~8.00 V/V (+18.06 dB) (or Predicted = 7.65 V/V = 17.67 dB).
# Target -3 dB point:
# If referenced to 18.06 dB: Target = 18.06 - 3.00 = 15.06 dB (|Av| = 8.00 / sqrt(2) = 5.66 V/V)
# If referenced to 17.73 dB: Target = 14.73 dB (|Av| = 5.44 V/V)
# If referenced to 18.28 dB: Target = 15.28 dB (|Av| = 5.80 V/V)
# Between 10 Hz (Gain = +4.08 dB, |Av| = 1.60) and 50 Hz (Gain = +18.28 dB, |Av| = 8.20):
f1, G1 = 10.0, 4.08
f2, G2 = 50.0, 18.28
G_target_10 = 18.06 - 3.00 # 15.06 dB
log_f_10 = np.log10(f1) + (G_target_10 - G1) / (G2 - G1) * (np.log10(f2) - np.log10(f1))
f_3db_low_10 = 10**log_f_10
print(f"\nGain of 10: Low-frequency -3 dB corner (between 10 Hz and 50 Hz, ref 18.06 dB): {f_3db_low_10:.2f} Hz")

# What about referenced to predicted 17.67 dB (target = 14.67 dB)?
G_target_10_pred = 17.67 - 3.00 # 14.67 dB
log_f_10_pred = np.log10(f1) + (G_target_10_pred - G1) / (G2 - G1) * (np.log10(f2) - np.log10(f1))
f_3db_low_10_pred = 10**log_f_10_pred
print(f"Gain of 10: Low-frequency -3 dB corner (ref predicted 17.67 dB): {f_3db_low_10_pred:.2f} Hz")

# Linear interpolation in f for Gain of 10:
f_lin_10 = f1 + (G_target_10 - G1) / (G2 - G1) * (f2 - f1)
print(f"Gain of 10: Low-frequency -3 dB corner (linear f interp): {f_lin_10:.2f} Hz")

# What about upper cutoff (above 700 Hz)?
# At 700 Hz: +18.06 dB
# At 1000 Hz: +11.71 dB (attenuation of 6.35 dB from 700 Hz!)
# So between 700 Hz and 1000 Hz, it drops past -3 dB!
f1, G1 = 700.0, 18.06
f2, G2 = 1000.0, 11.71
log_f_high_10 = np.log10(f1) + (G_target_10 - G1) / (G2 - G1) * (np.log10(f2) - np.log10(f1))
f_3db_high_10 = 10**log_f_high_10
print(f"Gain of 10: Upper -3 dB corner (between 700 Hz and 1000 Hz): {f_3db_high_10:.2f} Hz")

