import openpyxl
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams.update({
    'font.size': 11,
    'axes.labelsize': 12,
    'axes.titlesize': 13,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'legend.fontsize': 10,
    'lines.linewidth': 2.0,
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
del_id = np.array(del_id)
abs_del_id = np.array(abs_del_id)

VT = 0.02585
RD = 180.0
RSS = 22.0
ISS = 0.0801

pos_mask = vid > 0
neg_mask = vid < 0

# Fit region from 30 to 60 mV:
S_neg = (np.log(abs_del_id[neg_mask][-1]) - np.log(abs_del_id[neg_mask][-2])) / 0.03
S_pos = (np.log(abs_del_id[pos_mask][1]) - np.log(abs_del_id[pos_mask][0])) / 0.03
S_avg = (S_neg + S_pos) / 2.0
n_extracted = 1.0 / (2.0 * S_avg * VT) # = 1.235

# Plot 3: Semi-log plot of |del_ID| vs Vid
fig, ax = plt.subplots(figsize=(8.5, 5.5))
ax.semilogy(vid[pos_mask]*1e3, abs_del_id[pos_mask]*1e3, 'ro-', label=r'Measured $|\Delta I_D|$ for $V_{id} > 0$', markeredgewidth=1.5)
ax.semilogy(np.abs(vid[neg_mask])*1e3, abs_del_id[neg_mask]*1e3, 'bs-', label=r'Measured $|\Delta I_D|$ for $V_{id} < 0$', markeredgewidth=1.5)

# Fit lines in the subthreshold straight region (30-60 mV)
v_fit = np.linspace(25, 100, 50)
fit_pos_y = abs_del_id[pos_mask][0] * 1e3 * np.exp(S_pos * (v_fit - 30)*1e-3)
fit_neg_y = abs_del_id[neg_mask][-1] * 1e3 * np.exp(S_neg * (v_fit - 30)*1e-3)

ax.semilogy(v_fit, fit_pos_y, 'r--', alpha=0.8, label=rf'Weak-inversion fit ($V_{{id}}>0$, $S={S_pos:.2f}\,$V$^{{-1}}$)')
ax.semilogy(v_fit, fit_neg_y, 'b--', alpha=0.8, label=rf'Weak-inversion fit ($V_{{id}}<0$, $S={S_neg:.2f}\,$V$^{{-1}}$)')

ax.set_xlabel(r'Differential Input Magnitude $|V_{id}|$ (mV)')
ax.set_ylabel(r'Differential Current Magnitude $|\Delta I_D|$ (mA) [Log Scale]')
ax.set_title(r'Semi-Log Plot: $|\Delta I_D|$ vs $|V_{id}|$ (Exponential Weak-Inversion Test)')
ax.grid(True, which="both", ls="--")
ax.legend(loc='lower right', frameon=True)
plt.tight_layout()
fig.savefig('EXP_5/PLOTS/DIFF_MODE/abs_del_id_vs_vid_semilog.png', dpi=300)
plt.close()
print("Refined abs_del_id_vs_vid_semilog.png saved.")

# Plot 4: Linear plot with theoretical tanh overlay
vid_fine = np.linspace(-0.3, 0.3, 300)
del_id_plan = (ISS * 1e3) * np.tanh(vid_fine / (2 * 1.5 * VT))
del_id_fit = (ISS * 1e3) * np.tanh(vid_fine / (2 * n_extracted * VT))

fig, ax = plt.subplots(figsize=(9, 5.5))
ax.plot(vid*1e3, del_id*1e3, 'ko-', label=r'Experimental Measured $\Delta I_D = I_{D1} - I_{D2}$', zorder=4)
ax.plot(vid_fine*1e3, del_id_plan, 'b--', label=rf'Theoretical $\tanh$ (Planning $n=1.5, I_{{SS}}=80.1\,$mA)', linewidth=2)
ax.plot(vid_fine*1e3, del_id_fit, 'r-.', label=rf'Theoretical $\tanh$ (Extracted $n={n_extracted:.3f}, I_{{SS}}=80.1\,$mA)', linewidth=2)

ax.axhline(0, color='gray', linestyle=':', alpha=0.7)
ax.axvline(0, color='gray', linestyle=':', alpha=0.7)
ax.set_xlabel(r'Differential Input Voltage $V_{id} = V_{in+} - V_{cm}$ (mV)')
ax.set_ylabel(r'Differential Current $\Delta I_D$ (mA)')
ax.set_title(r'Differential Transfer Characteristic: Measured vs Theoretical $\tanh$')
ax.grid(True)
ax.legend(loc='upper left', frameon=True)
plt.tight_layout()
fig.savefig('EXP_5/PLOTS/DIFF_MODE/del_id_vs_vid_tanh_overlay.png', dpi=300)
plt.close()
print("Refined del_id_vs_vid_tanh_overlay.png saved.")
