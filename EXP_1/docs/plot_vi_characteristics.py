import gzip
import xml.etree.ElementTree as ET
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Set style
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams.update({
    'font.size': 12,
    'axes.labelsize': 14,
    'axes.titlesize': 14,
    'xtick.labelsize': 12,
    'ytick.labelsize': 12,
    'figure.titlesize': 16
})

# 1. Parse PN Diode Gnumeric XML
def parse_gnumeric(filepath):
    with gzip.open(filepath, 'rb') as f:
        tree = ET.parse(f)
    root = tree.getroot()
    ns = {'gnm': 'http://www.gnumeric.org/v10.dtd'}
    sheet = root.find('.//gnm:Sheet', ns)
    cells = {}
    for cell in sheet.findall('.//gnm:Cell', ns):
        r = int(cell.attrib['Row'])
        c = int(cell.attrib['Col'])
        val = cell.text
        cells[(r, c)] = val
    headers = [cells.get((0, c), '') for c in range(6)]
    data = []
    max_r = max(r for r, c in cells.keys())
    for r in range(1, max_r + 1):
        row = [cells.get((r, c), None) for c in range(6)]
        data.append(row)
    df = pd.DataFrame(data, columns=headers)
    return df

pn_df = parse_gnumeric('EXP_1/DIODE_READINGS/pn_diode_readings.csv')
pn_fwd = pn_df[['Forward_Vsup_V', 'Forward_Id_mA', 'Forward_Vd_V']].dropna().astype(float)
pn_rev = pn_df[['Reverse_Vsup_V', 'Reverse_Id', 'Reverse_Vd_V']].dropna().astype(float)

zener_fwd = pd.read_csv('EXP_1/ZENER_FORWARD_READINGS/zener_forward_readings.csv')
zener_rev = pd.read_csv('EXP_1/ZENER_REVERSE_READINGS/zener_reverse_readings.csv')

# --- 1. Linear Plots ---
# PN Diode Linear
fig, ax = plt.subplots(figsize=(8, 6))
ax.plot(pn_fwd['Forward_Vd_V'], pn_fwd['Forward_Id_mA'], 'bo-', label='Forward Bias')
ax.plot(pn_rev['Reverse_Vd_V'], pn_rev['Reverse_Id'], 'ro-', label='Reverse Bias')
ax.axhline(0, color='black', linewidth=0.8, linestyle='--')
ax.axvline(0, color='black', linewidth=0.8, linestyle='--')
ax.set_xscale('symlog', linthresh=1.0, linscale=1.0, base=10)
ax.set_xlabel('Diode Voltage $V_D$ (V)')
ax.set_ylabel('Diode Current $I_D$ (mA)')
ax.set_title('PN Junction Diode V-I Characteristics')
ax.legend(loc='upper left')
ax.grid(True, which='both')
plt.tight_layout()
plt.savefig('EXP_1/DIODE_READINGS/pn_diode_vi_linear.png', dpi=300)
plt.close()

# Zener Diode Linear
fig, ax = plt.subplots(figsize=(8, 6))
ax.plot(zener_fwd['Vz_V'], zener_fwd['Iz_mA'], 'go-', label='Forward Bias')
ax.plot(zener_rev['Vz_V'], zener_rev['Iz_mA'], 'mo-', label='Reverse Bias')
ax.axhline(0, color='black', linewidth=0.8, linestyle='--')
ax.axvline(0, color='black', linewidth=0.8, linestyle='--')
ax.set_xlabel('Zener Voltage $V_Z$ (V)')
ax.set_ylabel('Zener Current $I_Z$ (mA)')
ax.set_title('Zener Diode V-I Characteristics (Linear Scale)')
ax.legend(loc='lower left')
ax.grid(True)
plt.tight_layout()
plt.savefig('EXP_1/ZENER_FORWARD_READINGS/zener_diode_vi_linear.png', dpi=300)
plt.close()

# --- 2. Semi-Log Plots (Log for |I|, Linear for V) ---
# PN Diode Semi-Log
fig, ax = plt.subplots(figsize=(8, 6))
# Filter positive current for log scale
fwd_mask = pn_fwd['Forward_Id_mA'] > 0
ax.plot(pn_fwd.loc[fwd_mask, 'Forward_Vd_V'], pn_fwd.loc[fwd_mask, 'Forward_Id_mA'], 'bo-', label='Forward Bias')

rev_mask = abs(pn_rev['Reverse_Id']) > 0
if rev_mask.any():
    ax.plot(abs(pn_rev.loc[rev_mask, 'Reverse_Vd_V']), abs(pn_rev.loc[rev_mask, 'Reverse_Id']), 'ro-', label='Reverse Bias (|I|)')
else:
    # If all reverse currents are 0 in table, note it
    ax.scatter([], [], color='red', label='Reverse Bias ($I_R \approx 0\,\mu A$)')

ax.set_yscale('log')
ax.set_xlabel('Voltage $|V|$ (V)')
ax.set_ylabel('Current $|I|$ (mA) [Log Scale]')
ax.set_title('PN Junction Diode V-I Characteristics (Semi-Log Plot)')
ax.legend(loc='upper left')
ax.grid(True, which="both", ls="--")
plt.tight_layout()
plt.savefig('EXP_1/DIODE_READINGS/pn_diode_vi_semilog.png', dpi=300)
plt.close()

# Zener Diode Semi-Log
fig, ax = plt.subplots(figsize=(8, 6))
zf_mask = zener_fwd['Iz_mA'] > 0
ax.plot(zener_fwd.loc[zf_mask, 'Vz_V'], zener_fwd.loc[zf_mask, 'Iz_mA'], 'go-', label='Forward Bias')

zr_mask = abs(zener_rev['Iz_mA']) > 0
ax.plot(abs(zener_rev.loc[zr_mask, 'Vz_V']), abs(zener_rev.loc[zr_mask, 'Iz_mA']), 'mo-', label='Reverse Bias ($|I_Z|$)')

ax.set_yscale('log')
ax.set_xlabel('Voltage $|V|$ (V)')
ax.set_ylabel('Current $|I|$ (mA) [Log Scale]')
ax.set_title('Zener Diode V-I Characteristics (Semi-Log Plot)')
ax.legend(loc='upper left')
ax.grid(True, which="both", ls="--")
plt.tight_layout()
plt.savefig('EXP_1/ZENER_FORWARD_READINGS/zener_diode_vi_semilog.png', dpi=300)
plt.close()

print("Plots successfully created!")

