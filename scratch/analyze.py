import openpyxl
import numpy as np

wb = openpyxl.load_workbook('EXP_5/READINGS/DIFF_AMPLIFIER/EXP.xlsx', data_only=True)
ws3 = wb['Sheet3']
data = list(ws3.iter_rows(values_only=True))[1:]

v1 = []
vid = []
vd1 = []
vd2 = []
id1 = []
id2 = []
del_id = []
abs_del_id = []

for r in data:
    if r[0] is not None:
        v1.append(r[0])
        vid.append(r[1])
        vd1.append(r[2])
        vd2.append(r[3])
        id1.append(r[4])
        id2.append(r[5])
        del_id.append(r[6])
        abs_del_id.append(r[7])

v1 = np.array(v1, dtype=float)
vid = np.array(vid, dtype=float)
vd1 = np.array(vd1, dtype=float)
vd2 = np.array(vd2, dtype=float)
id1 = np.array(id1, dtype=float)
id2 = np.array(id2, dtype=float)
del_id = np.array(del_id, dtype=float)
abs_del_id = np.array(abs_del_id, dtype=float)

VT = 0.02585 # V
RD = 180.0 # ohms
RSS = 22.0 # ohms

print("Total points:", len(vid))
for i in range(len(vid)):
    print(f"Vid={vid[i]:+.3f} V, VD1={vd1[i]:.2f} V, VD2={vd2[i]:.2f} V, ID1={id1[i]*1e3:.2f} mA, ID2={id2[i]*1e3:.2f} mA, del_ID={del_id[i]*1e3:.2f} mA, |del_ID|={abs_del_id[i]*1e3:.2f} mA")

# Check log(|del_ID|)
# For Vid > 0:
pos_mask = vid > 0
neg_mask = vid < 0

print("\n--- Positive Vid ---")
for v, d in zip(vid[pos_mask], abs_del_id[pos_mask]):
    print(f"Vid={v:+.3f}, ln(|del_ID|)={np.log(d):.4f}, log10(|del_ID|)={np.log10(d):.4f}")

print("\n--- Negative Vid ---")
for v, d in zip(vid[neg_mask], abs_del_id[neg_mask]):
    print(f"Vid={v:+.3f}, ln(|del_ID|)={np.log(d):.4f}, log10(|del_ID|)={np.log10(d):.4f}")

# Check linear fit of ln(|del_ID|) vs |Vid| or Vid
# In weak inversion:
# If |del_ID| \propto exp(|Vid| / (2 n VT)) or exp(Vid / n VT)
# Let's test slope
slope_pos, intercept_pos = np.polyfit(vid[pos_mask][:3], np.log(abs_del_id[pos_mask][:3]), 1)
print(f"Pos Vid initial slope (ln): {slope_pos:.2f} -> if slope = 1/(n VT), n = {1/(slope_pos*VT):.2f}; if slope = 1/(2 n VT), n = {1/(2*slope_pos*VT):.2f}")

slope_neg, intercept_neg = np.polyfit(-vid[neg_mask][-3:], np.log(abs_del_id[neg_mask][-3:]), 1)
print(f"Neg Vid near zero slope (ln): {slope_neg:.2f} -> if slope = 1/(n VT), n = {1/(slope_neg*VT):.2f}; if slope = 1/(2 n VT), n = {1/(2*slope_neg*VT):.2f}")
