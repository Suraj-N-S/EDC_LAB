import openpyxl
import numpy as np
import matplotlib.pyplot as plt

# Set clean scientific plotting style
plt.rcParams.update({
    'font.size': 11,
    'axes.labelsize': 12,
    'axes.titlesize': 13,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'legend.fontsize': 10,
    'figure.titlesize': 14,
    'lines.linewidth': 1.8,
    'lines.markersize': 6,
    'grid.alpha': 0.6,
    'grid.linestyle': '--'
})

wb = openpyxl.load_workbook('EXP_5/READINGS/DIFF_AMPLIFIER/EXP.xlsx', data_only=True)
ws3 = wb['Sheet3']
data = list(ws3.iter_rows(values_only=True))[1:]

vid = []
del_id = []
abs_del_id = []

for r in data:
    if r[0] is not None:
        vid.append(float(r[1]))
        del_id.append(float(r[6]))
        abs_del_id.append(abs(float(r[6])))

vid = np.array(vid)
del_id = np.array(del_id) # in Amperes
abs_del_id = np.array(abs_del_id) # in Amperes

VT = 0.02585 # V (25.85 mV)
RD = 180.0 # Ohm
RSS = 22.0 # Ohm
ISS = 0.0801 # 80.1 mA from Q-point in Sheet1

# Point near Vid=0:
# Vid = -0.03 V (del_id = -7.167 mA), Vid = +0.03 V (del_id = +4.778 mA)
gm_meas = (0.004777777777777777 - (-0.0071666666666666615)) / (0.03 - (-0.03)) # A/V
print(f"gm(measured) = {gm_meas*1000:.2f} mA/V")

# Semi-log plot: |del_ID| vs Vid on semi-log axes (log Y, linear X)
# plotted separately for Vid > 0 and Vid < 0
pos_mask = vid > 0
neg_mask = vid < 0

# Let's fit straight line on semi-log for Vid > 0 and Vid < 0
# For Vid < 0, let's look at Vid from -0.03 to -0.15 or -0.30
# If log10(|del_ID|) vs Vid:
p_pos = np.polyfit(vid[pos_mask][:4], np.log(abs_del_id[pos_mask][:4]), 1)
p_neg = np.polyfit(np.abs(vid[neg_mask][-4:]), np.log(abs_del_id[neg_mask][-4:]), 1)

slope_pos_ln = p_pos[0]
slope_neg_ln = p_neg[0]
avg_slope_ln = (slope_pos_ln + slope_neg_ln) / 2.0

# If slope of ln(|del_ID|) vs |Vid| is taken as 1 / (2 n VT)
n_pos_2 = 1.0 / (2.0 * slope_pos_ln * VT)
n_neg_2 = 1.0 / (2.0 * slope_neg_ln * VT)
n_avg_2 = (n_pos_2 + n_neg_2) / 2.0

# If slope is taken as 1 / (n VT)
n_pos_1 = 1.0 / (slope_pos_ln * VT)
n_neg_1 = 1.0 / (slope_neg_ln * VT)
n_avg_1 = (n_pos_1 + n_neg_1) / 2.0

print(f"Slope pos (ln): {slope_pos_ln:.2f} -> n (factor 2): {n_pos_2:.3f}, n (factor 1): {n_pos_1:.3f}")
print(f"Slope neg (ln): {slope_neg_ln:.2f} -> n (factor 2): {n_neg_2:.3f}, n (factor 1): {n_neg_1:.3f}")
print(f"Average n: factor 2 -> {n_avg_2:.3f}, factor 1 -> {n_avg_1:.3f}")

# Plot 3: Semi-log plot of |del_ID| vs Vid
fig, ax = plt.subplots(figsize=(8, 5.5))
ax.semilogy(vid[pos_mask]*1e3, abs_del_id[pos_mask]*1e3, 'ro-', label=r'$V_{id} > 0$ (Measured $| \Delta I_D |$)', markeredgewidth=1.5)
ax.semilogy(np.abs(vid[neg_mask])*1e3, abs_del_id[neg_mask]*1e3, 'bs-', label=r'$V_{id} < 0$ (Measured $| \Delta I_D |$)', markeredgewidth=1.5)

# Add exponential trendline fits
vid_fine = np.linspace(30, 300, 100)
ax.semilogy(vid_fine, np.exp(p_pos[1] + p_pos[0]*vid_fine*1e-3)*1e3, 'r--', alpha=0.7, label=f'Exp Fit ($V_{{id}} > 0$), slope={slope_pos_ln:.1f} V$^{{-1}}$')
ax.semilogy(vid_fine, np.exp(p_neg[1] + p_neg[0]*vid_fine*1e-3)*1e3, 'b--', alpha=0.7, label=f'Exp Fit ($V_{{id}} < 0$), slope={slope_neg_ln:.1f} V$^{{-1}}$')

ax.set_xlabel(r'Differential Input Voltage $|V_{id}|$ (mV)')
ax.set_ylabel(r'Differential Current Magnitude $|\Delta I_D|$ (mA) [Log Scale]')
ax.set_title(r'Semi-Log Plot: $|\Delta I_D|$ vs $|V_{id}|$ (Weak Inversion Exponential Test)')
ax.grid(True, which="both", ls="--")
ax.legend(loc='lower right', frameon=True)
plt.tight_layout()
fig.savefig('EXP_5/PLOTS/DIFF_MODE/abs_del_id_vs_vid_semilog.png', dpi=300)
plt.close()
print("Saved abs_del_id_vs_vid_semilog.png")

# Plot 4: Linear plot with theoretical tanh overlay
# Let's generate theoretical curve with planning n=1.5 and extracted n
vid_theory = np.linspace(-0.3, 0.3, 200)
# Model: del_ID = ISS * tanh(Vid / (2 n VT))
# Planning estimate: ISS = 80.1 mA, n = 1.5
del_id_plan = (ISS * 1e3) * np.tanh(vid_theory / (2 * 1.5 * VT))
# With measured n:
# Let's also compute with fitted n or n=1.92
n_fit = n_avg_2
del_id_fit = (ISS * 1e3) * np.tanh(vid_theory / (2 * n_fit * VT))

fig, ax = plt.subplots(figsize=(8.5, 5.5))
ax.plot(vid*1e3, del_id*1e3, 'ko-', label=r'Measured $\Delta I_D = I_{D1} - I_{D2}$', zorder=4)
ax.plot(vid_theory*1e3, del_id_plan, 'b--', label=rf'Theoretical tanh (Planning $n=1.5, I_{{SS}}=80.1\,$mA)', linewidth=2)
ax.plot(vid_theory*1e3, del_id_fit, 'r-.', label=rf'Theoretical tanh (Extracted $n={n_fit:.2f}, I_{{SS}}=80.1\,$mA)', linewidth=2)

ax.axhline(0, color='gray', linestyle=':', alpha=0.7)
ax.axvline(0, color='gray', linestyle=':', alpha=0.7)
ax.set_xlabel(r'Differential Input Voltage $V_{id} = V_1 - V_2$ (mV)')
ax.set_ylabel(r'Differential Current $\Delta I_D$ (mA)')
ax.set_title(r'Differential Transfer Characteristic: Measured vs Theoretical $\tanh$')
ax.grid(True)
ax.legend(loc='best', frameon=True)
plt.tight_layout()
fig.savefig('EXP_5/PLOTS/DIFF_MODE/del_id_vs_vid_tanh_overlay.png', dpi=300)
plt.close()
print("Saved del_id_vs_vid_tanh_overlay.png")

