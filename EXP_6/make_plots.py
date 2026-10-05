import matplotlib.pyplot as plt
import numpy as np
import os

os.makedirs('/home/suraj-n/EDC_LAB/EXP_6/PLOTS', exist_ok=True)

# 1. Frequency response data
# Unity gain:
f_unity = np.array([5, 10, 50, 100, 200, 500, 700, 1000, 2000])
vin_unity = 100.0 # mV
vout1_unity = np.array([96, 72, 44, 100, 96, 54, 32, 100, 42]) # mV
vout2_unity = np.array([84, 76, 44, 100, 80, 44, 32, 100, 38]) # mV
# Differential output: Vout,diff = Vout1 + Vout2 (since 180 out of phase, diff amplitude is V1 + V2)
# Or differential gain: Av,diff = (Vout1 + Vout2) / (2 * Vin) if Vin is single-ended amplitude, or if Vin,diff = 2*Vin
# Let's compute:
vout_diff_unity = vout1_unity + vout2_unity
# If input is differential with each branch having amplitude Vin, Vin,diff = 2 * Vin = 200 mV
# Then Av,diff = (Vout1 + Vout2) / (2 * Vin)
gain_unity = vout_diff_unity / (2.0 * vin_unity)
gain_unity_db = 20 * np.log10(gain_unity)

# Gain of 10:
f_10 = np.array([5, 10, 50, 100, 200, 500, 700, 1000, 2000])
vin_10 = 20.0 # mV
vout1_10 = np.array([32, 37, 168, 64, 60, 156, 164, 80, 112])
vout2_10 = np.array([33, 27, 160, 46, 38, 152, 156, 74, 104])
vout_diff_10 = vout1_10 + vout2_10
gain_10 = vout_diff_10 / (2.0 * vin_10)
gain_10_db = 20 * np.log10(gain_10)

# Set style
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
fig, ax = plt.subplots(figsize=(8, 5), dpi=300)

ax.semilogx(f_unity, gain_unity_db, 'o-', color='#003366', linewidth=2, markersize=6, label='Unity Gain ($R_f=10\\,\\mathrm{k\\Omega}, R_{in}=10\\,\\mathrm{k\\Omega}$)')
ax.semilogx(f_10, gain_10_db, 's-', color='#d9534f', linewidth=2, markersize=6, label='Gain of 10 ($R_f=10\\,\\mathrm{k\\Omega}, R_{in}=1\\,\\mathrm{k\\Omega}$)')

# Reference lines for theoretical corner fc = 15.9 Hz
ax.axvline(15.9, color='gray', linestyle='--', alpha=0.7, label='Theoretical $f_c = 15.9\\,\\mathrm{Hz}$')

ax.set_title('Frequency Response: Closed-Loop Gain (dB) vs. Frequency', fontsize=12, fontweight='bold', pad=12)
ax.set_xlabel('Frequency (Hz) [Log Scale]', fontsize=11, fontweight='bold')
ax.set_ylabel('Differential Gain $A_{v,diff}$ (dB)', fontsize=11, fontweight='bold')
ax.grid(True, which="both", ls="--", alpha=0.5)
ax.legend(frameon=True, fontsize=10)
plt.tight_layout()
plt.savefig('/home/suraj-n/EDC_LAB/EXP_6/PLOTS/frequency_response_db.png')
plt.close()

# Also let's plot Gain Magnitude vs Frequency
fig, ax = plt.subplots(figsize=(8, 5), dpi=300)
ax.semilogx(f_unity, gain_unity, 'o-', color='#003366', linewidth=2, markersize=6, label='Unity Gain ($|A_v|$)')
ax.semilogx(f_10, gain_10, 's-', color='#d9534f', linewidth=2, markersize=6, label='Gain of 10 ($|A_v|$)')
ax.axvline(15.9, color='gray', linestyle='--', alpha=0.7, label='Theoretical $f_c = 15.9\\,\\mathrm{Hz}$')
ax.set_title('Frequency Response: Magnitude $|A_{v,diff}|$ vs. Frequency', fontsize=12, fontweight='bold', pad=12)
ax.set_xlabel('Frequency (Hz) [Log Scale]', fontsize=11, fontweight='bold')
ax.set_ylabel('Differential Gain Magnitude $|A_{v,diff}|$ (V/V)', fontsize=11, fontweight='bold')
ax.grid(True, which="both", ls="--", alpha=0.5)
ax.legend(frameon=True, fontsize=10)
plt.tight_layout()
plt.savefig('/home/suraj-n/EDC_LAB/EXP_6/PLOTS/frequency_response_mag.png')
plt.close()

# 2. Mid-band gain vs Ideal vs Predicted (Section 8 Graph 2)
# Ideal: Unity = 1.0, Gain 10 = 10.0
# Predicted (with Ad = 35.83): Unity = 0.947, Gain 10 = 7.651
# Measured (at 1 kHz or midband average):
# For unity gain: at Vin = 300, 400, 500 mV, gain is ~ 1.000 (at 1 kHz, f=1000, gain is 1.000)
# For gain of 10: at Vin = 50 mV, gain is 7.52; at 100 mV, gain is 7.40; at f=500 Hz, gain is 7.70; at f=700 Hz, gain is 8.00; at f=1000 Hz, gain is 3.85 (midband ~ 7.6)
# Let's make a clear comparison bar chart / scatter plot on the same axes as specified in section 8!
configs = ['Unity Gain\n($R_f/R_{in}=1$)', 'Gain of 10\n($R_f/R_{in}=10$)']
ideal_gains = [1.0, 10.0]
predicted_gains = [0.947, 7.651]
measured_gains = [1.000, 7.520] # at 50mV for gain 10, or average midband

x = np.arange(len(configs))
width = 0.25

fig, ax = plt.subplots(figsize=(7, 5), dpi=300)
rects1 = ax.bar(x - width, ideal_gains, width, label='Ideal ($R_f/R_{in}$)', color='#99ccff', edgecolor='#003366')
rects2 = ax.bar(x, predicted_gains, width, label='Predicted (with $A_d=35.83$)', color='#4682b4', edgecolor='#003366')
rects3 = ax.bar(x + width, measured_gains, width, label='Measured (Experimental)', color='#003366', edgecolor='#001a33')

ax.set_ylabel('Gain Magnitude $|A_v|$ (V/V)', fontsize=11, fontweight='bold')
ax.set_title('Comparison of Ideal, Predicted, and Measured Mid-Band Gain', fontsize=12, fontweight='bold', pad=12)
ax.set_xticks(x)
ax.set_xticklabels(configs, fontsize=11, fontweight='bold')
ax.grid(True, axis='y', ls='--', alpha=0.5)
ax.legend(frameon=True, fontsize=10)

def autolabel(rects):
    for rect in rects:
        height = rect.get_height()
        ax.annotate(f'{height:.2f}',
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=9, fontweight='bold')

autolabel(rects1)
autolabel(rects2)
autolabel(rects3)

plt.tight_layout()
plt.savefig('/home/suraj-n/EDC_LAB/EXP_6/PLOTS/midband_gain_comparison.png')
plt.close()

# 3. Linearity / Gain vs Vin plot for Section 6.2 and 6.3
vin_u = np.array([50, 150, 300, 400, 500])
vout_diff_u = np.array([64+64, 168+158, 304+296, 400+392, 512+488])
gain_u_vin = vout_diff_u / (2.0 * vin_u)

fig, ax1 = plt.subplots(figsize=(7, 4.5), dpi=300)
ax1.plot(vin_u, vout_diff_u, 'o-', color='#003366', linewidth=2, label='$V_{out,diff}$')
ax1.set_xlabel('Input Amplitude $V_{in}$ (mV)', fontsize=10, fontweight='bold')
ax1.set_ylabel('Differential Output $V_{out,diff}$ (mV)', color='#003366', fontsize=10, fontweight='bold')
ax1.tick_params(axis='y', labelcolor='#003366')
ax1.grid(True, ls='--', alpha=0.5)

ax2 = ax1.twinx()
ax2.plot(vin_u, gain_u_vin, 's--', color='#d9534f', linewidth=2, label='Measured Gain $|A_v|$')
ax2.axhline(0.947, color='green', linestyle=':', label='Predicted $|A_v|=0.947$')
ax2.set_ylabel('Measured Gain $|A_v|$ (V/V)', color='#d9534f', fontsize=10, fontweight='bold')
ax2.tick_params(axis='y', labelcolor='#d9534f')
ax2.set_ylim([0.8, 1.4])

plt.title('Unity-Gain Configuration: Linearity & Gain vs. $V_{in}$', fontsize=11, fontweight='bold', pad=10)
fig.tight_layout()
plt.savefig('/home/suraj-n/EDC_LAB/EXP_6/PLOTS/unity_gain_vs_vin.png')
plt.close()

vin_10_arr = np.array([5, 20, 50, 100])
vout_diff_10_arr = np.array([51.2+44, 164+160, 392+360, 780+700])
gain_10_vin = vout_diff_10_arr / (2.0 * vin_10_arr)

fig, ax1 = plt.subplots(figsize=(7, 4.5), dpi=300)
ax1.plot(vin_10_arr, vout_diff_10_arr, 'o-', color='#003366', linewidth=2, label='$V_{out,diff}$')
ax1.set_xlabel('Input Amplitude $V_{in}$ (mV)', fontsize=10, fontweight='bold')
ax1.set_ylabel('Differential Output $V_{out,diff}$ (mV)', color='#003366', fontsize=10, fontweight='bold')
ax1.tick_params(axis='y', labelcolor='#003366')
ax1.grid(True, ls='--', alpha=0.5)

ax2 = ax1.twinx()
ax2.plot(vin_10_arr, gain_10_vin, 's--', color='#d9534f', linewidth=2, label='Measured Gain $|A_v|$')
ax2.axhline(7.651, color='green', linestyle=':', label='Predicted $|A_v|=7.651$')
ax2.set_ylabel('Measured Gain $|A_v|$ (V/V)', color='#d9534f', fontsize=10, fontweight='bold')
ax2.tick_params(axis='y', labelcolor='#d9534f')
ax2.set_ylim([6.0, 11.0])

plt.title('Gain-of-10 Configuration: Linearity & Gain vs. $V_{in}$', fontsize=11, fontweight='bold', pad=10)
fig.tight_layout()
plt.savefig('/home/suraj-n/EDC_LAB/EXP_6/PLOTS/gain10_vs_vin.png')
plt.close()

print('Plots generated successfully!')
