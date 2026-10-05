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
ax.set_title('Frequency Response: Closed-Loop Differential Gain (dB) vs. Frequency', fontsize=12, fontweight='bold', pad=12)
ax.set_xlabel('Frequency (Hz) [Logarithmic Scale]', fontsize=11, fontweight='bold')
ax.set_ylabel('Differential Gain $A_{v,diff}$ (dB)', fontsize=11, fontweight='bold')
ax.grid(True, which="both", ls="--", alpha=0.5)
ax.legend(frameon=True, fontsize=9)
plt.tight_layout()
plt.savefig('/home/suraj-n/EDC_LAB/EXP_6/PLOTS/frequency_response_db.png')
plt.close()

# Separate Frequency response for Unity Gain
fig, ax = plt.subplots(figsize=(7, 4.2), dpi=300)
ax.semilogx(f_unity, gain_unity_db, 'o-', color='#003366', linewidth=2, markersize=6, label='Measured Gain (dB)')
ax.axhline(0, color='gray', linestyle=':', label='Ideal 0 dB ($|A_v|=1$)')
ax.axvline(8.84, color='orange', linestyle='--', label='Theoretical $f_c = 8.84\\,\\mathrm{Hz}$')
ax.set_title('Unity Gain Configuration: Frequency Response ($C_{in}=1\\,\\mu\\mathrm{F}, C_f=1\\,\\mu\\mathrm{F}$)', fontsize=11, fontweight='bold', pad=10)
ax.set_xlabel('Frequency (Hz) [Log Scale]', fontsize=10, fontweight='bold')
ax.set_ylabel('Gain $A_{v,diff}$ (dB)', fontsize=10, fontweight='bold')
ax.grid(True, which="both", ls="--", alpha=0.5)
ax.legend(frameon=True, fontsize=9)
plt.tight_layout()
plt.savefig('/home/suraj-n/EDC_LAB/EXP_6/PLOTS/unity_freq_resp.png')
plt.close()

# Separate Frequency response for Gain of 10
fig, ax = plt.subplots(figsize=(7, 4.2), dpi=300)
ax.semilogx(f_10, gain_10_db, 's-', color='#d9534f', linewidth=2, markersize=6, label='Measured Gain (dB)')
ax.axhline(20, color='gray', linestyle=':', label='Ideal 20 dB ($|A_v|=10$)')
ax.axhline(17.67, color='green', linestyle='--', label='Predicted 17.67 dB ($|A_v|=7.65$)')
ax.axvline(0.88, color='purple', linestyle='--', label='Theoretical $f_c = 0.88\\,\\mathrm{Hz}$')
ax.set_title('Gain-of-10 Configuration: Frequency Response ($C_{in}=10\\,\\mu\\mathrm{F}, C_f=1\\,\\mu\\mathrm{F}$)', fontsize=11, fontweight='bold', pad=10)
ax.set_xlabel('Frequency (Hz) [Log Scale]', fontsize=10, fontweight='bold')
ax.set_ylabel('Gain $A_{v,diff}$ (dB)', fontsize=10, fontweight='bold')
ax.grid(True, which="both", ls="--", alpha=0.5)
ax.legend(frameon=True, fontsize=9)
plt.tight_layout()
plt.savefig('/home/suraj-n/EDC_LAB/EXP_6/PLOTS/gain10_freq_resp.png')
plt.close()

# Mid-band gain comparison
configs = ['Unity Gain\n($18\\,\\mathrm{k\\Omega} / 18\\,\\mathrm{k\\Omega}$)', 'Gain of 10\n($180\\,\\mathrm{k\\Omega} / 18\\,\\mathrm{k\\Omega}$)']
ideal_gains = [1.0, 10.0]
predicted_gains = [0.947, 7.651]
measured_gains = [1.000, 7.520]

x = np.arange(len(configs))
width = 0.25

fig, ax = plt.subplots(figsize=(7, 4.8), dpi=300)
rects1 = ax.bar(x - width, ideal_gains, width, label='Ideal ($R_f/R_{in}$)', color='#99ccff', edgecolor='#003366')
rects2 = ax.bar(x, predicted_gains, width, label='Predicted ($A_d=35.83$)', color='#4682b4', edgecolor='#003366')
rects3 = ax.bar(x + width, measured_gains, width, label='Measured Experimental', color='#003366', edgecolor='#001a33')

ax.set_ylabel('Gain Magnitude $|A_v|$ (V/V)', fontsize=11, fontweight='bold')
ax.set_title('Comparison of Ideal, Predicted, and Measured Mid-Band Gain', fontsize=12, fontweight='bold', pad=12)
ax.set_xticks(x)
ax.set_xticklabels(configs, fontsize=11, fontweight='bold')
ax.grid(True, axis='y', ls='--', alpha=0.5)
ax.legend(frameon=True, fontsize=10)

for rect in rects1:
    h = rect.get_height()
    ax.annotate(f'{h:.2f}', xy=(rect.get_x() + rect.get_width()/2, h), xytext=(0, 3), textcoords="offset points", ha='center', va='bottom', fontsize=9, fontweight='bold')
for rect in rects2:
    h = rect.get_height()
    ax.annotate(f'{h:.2f}', xy=(rect.get_x() + rect.get_width()/2, h), xytext=(0, 3), textcoords="offset points", ha='center', va='bottom', fontsize=9, fontweight='bold')
for rect in rects3:
    h = rect.get_height()
    ax.annotate(f'{h:.2f}', xy=(rect.get_x() + rect.get_width()/2, h), xytext=(0, 3), textcoords="offset points", ha='center', va='bottom', fontsize=9, fontweight='bold')

plt.tight_layout()
plt.savefig('/home/suraj-n/EDC_LAB/EXP_6/PLOTS/midband_gain_comparison.png')
plt.close()

print('Updated plots generated successfully!')
