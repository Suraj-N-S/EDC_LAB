import openpyxl
import pandas as pd
import numpy as np

wb = openpyxl.load_workbook('/home/suraj-n/EDC_LAB/EXP_6/READINGS/CLOSED_LOOP.xlsx', data_only=True)
ws = wb['Sheet1']

# Rows 2 to 6: Unity Gain vs Vin
# Header: Row 1: ['UNITY GAIN', None, 'VIN(mV)', 'VOUT1(mV', 'VOUT2(mV)']
unity_vin_rows = []
for r in range(2, 7):
    vin = ws.cell(r, 3).value
    vout1 = ws.cell(r, 4).value
    vout2 = ws.cell(r, 5).value
    unity_vin_rows.append((vin, vout1, vout2))

print("Unity Gain - Vin Variation (at 1 kHz or midband):")
print("Vin(mV) | Vout1(mV) | Vout2(mV) | Vout,diff = Vout1 + Vout2 (mV) | |Vout1 - (-Vout2)| | Gain = Vout,diff/Vin")
for vin, v1, v2 in unity_vin_rows:
    # Since Vout1 and Vout2 are 180 deg out of phase:
    # If Vout1 is positive amplitude and Vout2 is positive amplitude,
    # the differential output Vout,diff = Vout1 - Vout2 has peak/amplitude = Vout1 + Vout2 (or 2*Vout if symmetric)
    # Or is Vin differential or single ended? Let's check!
    # If AFG gives Vin, what is Vin?
    # In table: Vin = 50, 150, 300, 400, 500 mV.
    # Vout1 = 64, 168, 304, 400, 512 mV.
    # Vout2 = 64, 158, 296, 392, 488 mV.
    # Notice that Vout1 ~= Vin and Vout2 ~= Vin!
    # So single-ended gain Vout1/Vin ~= 1.0!
    # If Vin is single-ended or each branch input is Vin, let's see!
    print(f"{vin:6} | {v1:9} | {v2:9} | Vout1/Vin = {v1/vin:.3f} | Vout2/Vin = {v2/vin:.3f} | (V1+V2)/(2*Vin) = {(v1+v2)/(2*vin):.3f} | (V1+V2)/Vin = {(v1+v2)/vin:.3f}")

# Rows 10 to 18: Unity Gain Frequency Sweep
# Header: Row 9: ['FREQ(Hz)', 'VIN amp(mV)', 'VOUT1 amp(mV)', 'VOUT2 amp(mV)', None]
unity_freq_rows = []
for r in range(10, 19):
    f = ws.cell(r, 1).value
    vin = ws.cell(r, 2).value
    v1 = ws.cell(r, 3).value
    v2 = ws.cell(r, 4).value
    unity_freq_rows.append((f, vin, v1, v2))

print("\nUnity Gain - Frequency Sweep:")
print("Freq(Hz) | Vin(mV) | Vout1(mV) | Vout2(mV) | Vout,avg | Av_single | Av_diff_ratio")
for f, vin, v1, v2 in unity_freq_rows:
    print(f"{f:8} | {vin:7} | {v1:9} | {v2:9} | {(v1+v2)/2:.1f} | {((v1+v2)/2)/vin:.3f} | {(v1+v2)/vin:.3f}")

# Rows 22 to 25: Gain 10 vs Vin
# Header: Row 21: ['GAIN 10', None, 'VIN(mV)', 'VOUT1(mV', 'VOUT2(mV)']
gain10_vin_rows = []
for r in range(22, 26):
    vin = ws.cell(r, 3).value
    v1 = ws.cell(r, 4).value
    v2 = ws.cell(r, 5).value
    gain10_vin_rows.append((vin, v1, v2))

print("\nGain 10 - Vin Variation:")
for vin, v1, v2 in gain10_vin_rows:
    print(f"{vin:6} | {v1:9} | {v2:9} | Vout1/Vin = {v1/vin:.3f} | Vout2/Vin = {v2/vin:.3f} | Vout_avg/Vin = {((v1+v2)/2)/vin:.3f} | (V1+V2)/Vin = {(v1+v2)/vin:.3f}")

# Rows 28 to 36: Gain 10 Frequency Sweep
# Header: Row 27: ['FREQ(Hz)', 'VIN amp(mV)', 'VOUT1(mV)', 'VOUT2(mV)', None]
gain10_freq_rows = []
for r in range(28, 37):
    f = ws.cell(r, 1).value
    vin = ws.cell(r, 2).value
    v1 = ws.cell(r, 3).value
    v2 = ws.cell(r, 4).value
    gain10_freq_rows.append((f, vin, v1, v2))

print("\nGain 10 - Frequency Sweep:")
for f, vin, v1, v2 in gain10_freq_rows:
    print(f"{f:8} | {vin:7} | {v1:9} | {v2:9} | {(v1+v2)/2:.1f} | {((v1+v2)/2)/vin:.3f} | {(v1+v2)/vin:.3f}")

