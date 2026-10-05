import matplotlib.pyplot as plt
import numpy as np
import os

os.makedirs('/home/suraj-n/EDC_LAB/EXP_6/PLOTS', exist_ok=True)

# 1. Frequency response data
f_unity = np.array([5, 10, 50, 100, 200, 500, 700, 1000, 2000])
vin_unity = 100.0 # mV
vout1_unity = np.array([96, 72, 44, 100, 96, 54, 32, 100, 42]) # mV
vout2_unity = np.array([84, 76, 44, 100, 80, 44, 32, 100, 38]) # mV
vout_diff_unity = vout1_unity + vout2_unity
gain_unity = vout_diff_unity / (2.0 * vin_unity)
gain_unity_db = 20 * np.log10(gain_unity)

f_10 = np.array([5, 10, 50, 100, 200, 500, 700, 1000, 2000])
vin_10 = 20.0 # mV
vout1_10 = np.array([32, 37, 168, 64, 60, 156, 164, 80, 112])
vout2_10 = np.array([33, 27, 160, 46, 38, 152, 156, 74, 104])
vout_diff_10 = vout1_10 + vout2_10
gain_10 = vout_diff_10 / (2.0 * vin_10)
gain_10_db = 20 * np.log10(gain_10)

plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')

# Combined Frequency response
fig, ax = plt.subplots(figsize=(8, 4.8), dpi=300)
ax.semilogx(f_unity, gain_unity_db, 'o-', color='#003366', linewidth=2, markersize=6, label='Unity Gain ($R_f=18\\,\\mathrm{k\\Omega}, C_f=1\\,\\mu\\mathrm{F}; R_{in}=18\\,\\mathrm{k\\Omega}, C_{in}=1\\,\\mu\\mathrm{F}$)')
ax.semilogx(f_10, gain_10_db, 's-', color='#d9534f', linewidth=2, markersize=6, label='Gain of 10 ($R_f=180\\,\\mathrm{k\\Omega}, C_f=1\\,\\mu\\mathrm{F}; R_{in}=18\\,\\mathrm{k\\Omega}, C_{in}=10\\,\\mu\\mathrm{F}$)')
ax.axhline(-3.0, color='#003366', linestyle=':', alpha=0.6, label='Unity $-3\\,\\mathrm{dB}$ Level ($-3\\,\\mathrm{dB}$)')
ax.axhline(15.06, color='#d9534f', linestyle=':', alpha=0.6, label='Gain of 10 $-3\\,\\mathrm{dB}$ Level ($+15.06\\,\\mathrm{dB}$)')
ax.set_title('Frequency Response: Closed-Loop Differential Gain (dB) vs. Frequency', fontsize=12, fontweight='bold', pad=12)
ax.set_xlabel('Frequency (Hz) [Logarithmic Scale]', fontsize=11, fontweight='bold')
ax.set_ylabel('Differential Gain $A_{v,diff}$ (dB)', fontsize=11, fontweight='bold')
ax.grid(True, which="both", ls="--", alpha=0.5)
ax.legend(frameon=True, fontsize=8.5, loc='lower left')
plt.tight_layout()
plt.savefig('/home/suraj-n/EDC_LAB/EXP_6/PLOTS/frequency_response_db.png')
plt.close()

# Separate Frequency response for Unity Gain with -3dB annotations
fig, ax = plt.subplots(figsize=(7, 4.2), dpi=300)
ax.semilogx(f_unity, gain_unity_db, 'o-', color='#003366', linewidth=2, markersize=6, label='Measured Gain (dB)')
ax.axhline(0, color='gray', linestyle='-', alpha=0.5, label='Midband 0 dB ($|A_v|=1.0$)')
ax.axhline(-3.0, color='red', linestyle='--', alpha=0.8, label='$-3\\,\\mathrm{dB}$ Level ($-3.0\\,\\mathrm{dB}, |A_v|=0.707$)')
ax.axvline(10.5, color='orange', linestyle='--', label='Est. $f_{-3\\mathrm{dB,low}} \\approx 10.5\\,\\mathrm{Hz}$')
ax.plot(10, -2.62, 'ro', markersize=8)
ax.annotate('10 Hz: -2.62 dB\n(Near -3 dB)', xy=(10, -2.62), xytext=(12, -4.5),
            arrowprops=dict(facecolor='black', shrink=0.08, width=1, headwidth=5),
            fontsize=8.5, fontweight='bold')
ax.set_title('Unity Gain Configuration: Frequency Response & $-3\\,\\mathrm{dB}$ Corner', fontsize=11, fontweight='bold', pad=10)
ax.set_xlabel('Frequency (Hz) [Log Scale]', fontsize=10, fontweight='bold')
ax.set_ylabel('Gain $A_{v,diff}$ (dB)', fontsize=10, fontweight='bold')
ax.grid(True, which="both", ls="--", alpha=0.5)
ax.legend(frameon=True, fontsize=8.5, loc='lower left')
plt.tight_layout()
plt.savefig('/home/suraj-n/EDC_LAB/EXP_6/PLOTS/unity_freq_resp.png')
plt.close()

# Separate Frequency response for Gain of 10 with -3dB annotations
fig, ax = plt.subplots(figsize=(7, 4.2), dpi=300)
ax.semilogx(f_10, gain_10_db, 's-', color='#d9534f', linewidth=2, markersize=6, label='Measured Gain (dB)')
ax.axhline(18.06, color='gray', linestyle='-', alpha=0.5, label='Midband Peak $+18.06\\,\\mathrm{dB}$ ($|A_v|=8.0$)')
ax.axhline(15.06, color='red', linestyle='--', alpha=0.8, label='$-3\\,\\mathrm{dB}$ Level ($+15.06\\,\\mathrm{dB}, |A_v|=5.66$)')
ax.axvline(34.7, color='purple', linestyle='--', label='Est. $f_{-3\\mathrm{dB,low}} \\approx 34.7\\,\\mathrm{Hz}$')
ax.annotate('Est. -3 dB Corner:\n$f_{-3\\mathrm{dB}} \\approx 34.7\\,\\mathrm{Hz}$', xy=(34.7, 15.06), xytext=(12, 12.0),
            arrowprops=dict(facecolor='purple', shrink=0.08, width=1, headwidth=5),
            fontsize=8.5, fontweight='bold')
ax.set_title('Gain-of-10 Configuration: Frequency Response & $-3\\,\\mathrm{dB}$ Corner', fontsize=11, fontweight='bold', pad=10)
ax.set_xlabel('Frequency (Hz) [Log Scale]', fontsize=10, fontweight='bold')
ax.set_ylabel('Gain $A_{v,diff}$ (dB)', fontsize=10, fontweight='bold')
ax.grid(True, which="both", ls="--", alpha=0.5)
ax.legend(frameon=True, fontsize=8.5, loc='lower right')
plt.tight_layout()
plt.savefig('/home/suraj-n/EDC_LAB/EXP_6/PLOTS/gain10_freq_resp.png')
plt.close()

print('Updated frequency response plots with -3dB annotations generated successfully!')
