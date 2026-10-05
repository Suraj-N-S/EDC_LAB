import numpy as np

# Unity Gain Data:
# f = [5, 10, 50, 100, 200, 500, 700, 1000, 2000]
# Vin = 100 mV
# Vout1 = [96, 72, 44, 100, 96, 54, 32, 100, 42]
# Vout2 = [84, 76, 44, 100, 80, 44, 32, 100, 38]
# Vout,diff = Vout1 + Vout2
# Gain |Av| = (Vout1 + Vout2) / (2 * Vin)
f_u = np.array([5, 10, 50, 100, 200, 500, 700, 1000, 2000], dtype=float)
v1_u = np.array([96, 72, 44, 100, 96, 54, 32, 100, 42], dtype=float)
v2_u = np.array([84, 76, 44, 100, 80, 44, 32, 100, 38], dtype=float)
vdiff_u = v1_u + v2_u
gain_u = vdiff_u / 200.0
gain_u_db = 20 * np.log10(gain_u)

print("=== UNITY GAIN ===")
for i in range(len(f_u)):
    print(f"f = {f_u[i]:5.0f} Hz: Vdiff = {vdiff_u[i]:5.1f} mV, |Av| = {gain_u[i]:.4f}, Gain(dB) = {gain_u_db[i]:+6.2f} dB")

# Midband gain for Unity: at 100 Hz and 1000 Hz, |Av| = 1.000 (0 dB).
# -3 dB point means Gain = 0 dB - 3 dB = -3.00 dB, or |Av| = 1.000 / sqrt(2) = 0.7071 V/V.
# At 10 Hz: |Av| = 0.740, Gain = -2.62 dB
# At 5 Hz:  |Av| = 0.900 (wait, at 5 Hz, |Av| is 0.900, at 10 Hz is 0.740)
# Wait, why is it 0.900 at 5 Hz? In experimental measurements, let's see.
# Or if it rolls off at high frequency too:
# At 200 Hz: -1.11 dB
# At 500 Hz: -6.20 dB
# Between 200 Hz and 500 Hz, it crosses -3 dB!
# Let's check linear and log interpolation:
# Between 10 Hz (-2.62 dB) and 50 Hz (-7.13 dB):
# Or between 5 Hz and 10 Hz?
# Let's check all crossings of -3 dB!

# Gain of 10 Data:
f_10 = np.array([5, 10, 50, 100, 200, 500, 700, 1000, 2000], dtype=float)
v1_10 = np.array([32, 37, 168, 64, 60, 156, 164, 80, 112], dtype=float)
v2_10 = np.array([33, 27, 160, 46, 38, 152, 156, 74, 104], dtype=float)
vdiff_10 = v1_10 + v2_10
gain_10 = vdiff_10 / 40.0
gain_10_db = 20 * np.log10(gain_10)

print("\n=== GAIN OF 10 ===")
for i in range(len(f_10)):
    print(f"f = {f_10[i]:5.0f} Hz: Vdiff = {vdiff_10[i]:5.1f} mV, |Av| = {gain_10[i]:.4f}, Gain(dB) = {gain_10_db[i]:+6.2f} dB")

