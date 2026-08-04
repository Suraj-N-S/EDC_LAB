import gzip
import xml.etree.ElementTree as ET
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

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

# Clean PN Diode data
pn_fwd = pn_df[['Forward_Vsup_V', 'Forward_Id_mA', 'Forward_Vd_V']].dropna().astype(float)
pn_rev = pn_df[['Reverse_Vsup_V', 'Reverse_Id', 'Reverse_Vd_V']].dropna().astype(float)

# Zener Data
zener_fwd = pd.read_csv('EXP_1/ZENER_FORWARD_READINGS/zener_forward_readings.csv')
zener_rev = pd.read_csv('EXP_1/ZENER_REVERSE_READINGS/zener_reverse_readings.csv')

print("PN Forward:")
print(pn_fwd)
print("\nPN Reverse:")
print(pn_rev)
print("\nZener Forward:")
print(zener_fwd)
print("\nZener Reverse:")
print(zener_rev)

