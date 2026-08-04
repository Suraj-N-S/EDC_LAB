import pandas as pd
import numpy as np
import gzip
import xml.etree.ElementTree as ET

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

print("--- PN Diode Calculations ---")
# Static forward resistance R_DC = Vd / Id
# Let's compute at last reading (Vd=0.73V, Id=20mA) and near knee (Vd=0.63V, Id=2.22mA)
for idx in [11, 15, 20]:
    row = pn_fwd.iloc[idx]
    vd, id_ma = row['Forward_Vd_V'], row['Forward_Id_mA']
    r_dc = (vd / (id_ma * 1e-3)) if id_ma > 0 else np.nan
    print(f"At Vd={vd}V, Id={id_ma}mA: R_DC = {r_dc:.2f} Ohms")

# Dynamic forward resistance r_d = delta Vd / delta Id
# Between idx 19 and 20 (or idx 15 and 16)
p1 = pn_fwd.iloc[15] # Vd=0.70, Id=10.22mA
p2 = pn_fwd.iloc[20] # Vd=0.73, Id=20.0mA
rd = (p2['Forward_Vd_V'] - p1['Forward_Vd_V']) / ((p2['Forward_Id_mA'] - p1['Forward_Id_mA']) * 1e-3)
print(f"Dynamic resistance r_d (10.22mA to 20mA): {rd:.2f} Ohms")

p1_knee = pn_fwd.iloc[11] # Vd=0.63, Id=2.22mA
p2_knee = pn_fwd.iloc[12] # Vd=0.66, Id=4.22mA
rd_knee = (p2_knee['Forward_Vd_V'] - p1_knee['Forward_Vd_V']) / ((p2_knee['Forward_Id_mA'] - p1_knee['Forward_Id_mA']) * 1e-3)
print(f"Dynamic resistance r_d (2.22mA to 4.22mA): {rd_knee:.2f} Ohms")

print("Reverse Saturation Current Is = 0.0 uA / < 1 uA (0 mA measured in table up to 30V)")

print("\n--- Zener Diode Calculations ---")
# Zener breakdown voltage V_Z is approx 5.0V to 5.25V. At Iz = 20mA, Vz = 5.25V. At Iz = 2.8mA, Vz = 5.0V.
# Zener resistance R_Z = delta Vz / delta Iz in breakdown region (from Iz = 2.8mA to 20mA)
z_bd1 = zener_rev.iloc[24] # Vz = -5.00V, Iz = -2.8mA
z_bd2 = zener_rev.iloc[33] # Vz = -5.25V, Iz = -20.0mA
rz = (abs(z_bd2['Vz_V']) - abs(z_bd1['Vz_V'])) / ((abs(z_bd2['Iz_mA']) - abs(z_bd1['Iz_mA'])) * 1e-3)
print(f"Zener Breakdown Voltage V_Z ~ {abs(z_bd1['Vz_V']):.2f} V to {abs(z_bd2['Vz_V']):.2f} V")
print(f"Zener Resistance R_Z (between 2.8mA and 20mA): {rz:.2f} Ohms")

