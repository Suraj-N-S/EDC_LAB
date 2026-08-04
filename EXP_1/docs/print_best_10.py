import pandas as pd
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

# Select 10 representative points across the range for PN fwd
pn_fwd_10_indices = [0, 4, 6, 8, 10, 11, 13, 15, 17, 20]
pn_fwd_10 = pn_fwd.iloc[pn_fwd_10_indices]

# PN rev has 7 points
pn_rev_7 = pn_rev

# Zener fwd has 11 points - pick 10
zener_fwd_10 = zener_fwd.iloc[[0, 1, 3, 5, 6, 7, 8, 9, 10]] # 9/10 points

# Zener rev has 34 points - pick 10 across key regions (pre-breakdown, knee, breakdown)
zener_rev_10_indices = [0, 2, 5, 7, 9, 15, 19, 23, 27, 33]
zener_rev_10 = zener_rev.iloc[zener_rev_10_indices]

print("=== PN FORWARD BEST 10 ===")
print(pn_fwd_10.to_string(index=False))

print("\n=== PN REVERSE READINGS ===")
print(pn_rev_7.to_string(index=False))

print("\n=== ZENER FORWARD READINGS ===")
print(zener_fwd_10.to_string(index=False))

print("\n=== ZENER REVERSE BEST 10 ===")
print(zener_rev_10.to_string(index=False))

