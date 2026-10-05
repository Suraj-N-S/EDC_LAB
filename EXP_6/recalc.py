import numpy as np

Ad = 35.83

# User components:
# Unity Gain: Rin = 18k, Rf = 18k
# Gain of 10: Rin = 18k, Rf = 180k
# Let's check coupling capacitors:
# In LTspice file:
# C1 = 10uF, C2 = 10uF, C3 = 1uF, C4 = 1uF
# R8 = 180k (Rf), R9 = 180k (Rf), R6 = 18k (Rin), R7 = 18k (Rin)
# For Unity: Rf = 18k, Rin = 18k
# beta = Rin / (Rf + Rin)
beta_u = 18.0 / (18.0 + 18.0) # 0.5
T_u = Ad * beta_u # 35.83 * 0.5 = 17.915
Av_ideal_u = - 18.0 / 18.0 # -1.0
Av_pred_u = - Ad * 18.0 / (18.0 + 18.0 * (1 + Ad)) # -35.83 / 37.83 = -0.9471 V/V

# For Gain 10: Rf = 180k, Rin = 18k
beta_10 = 18.0 / (180.0 + 18.0) # 18/198 = 1/11 = 0.090909...
T_10 = Ad * beta_10 # 35.83 / 11 = 3.2573
Av_ideal_10 = - 180.0 / 18.0 # -10.0
Av_pred_10 = - Ad * 180.0 / (180.0 + 18.0 * (1 + Ad)) # - 35.83 * 10 / (10 + 1 + 35.83) = -358.3 / 46.83 = -7.6511 V/V

print(f"Unity Gain: Rin=18k, Rf=18k, beta={beta_u:.4f}, T={T_u:.4f}, Ideal={Av_ideal_u:.2f}, Pred={Av_pred_u:.4f}")
print(f"Gain 10: Rin=18k, Rf=180k, beta={beta_10:.4f}, T={T_10:.4f}, Ideal={Av_ideal_10:.2f}, Pred={Av_pred_10:.4f}")

# Corner frequency:
# With Cin = 10 uF and Rin = 18k:
# fc = 1 / (2 * pi * 18e3 * 10e-6) = 1 / (2 * pi * 0.18) = 0.884 Hz
# If Cin = 1 uF and Rin = 18k:
# fc = 1 / (2 * pi * 18e3 * 1e-6) = 1 / (2 * pi * 0.018) = 8.84 Hz
# If Cf = 1 uF and Rf = 180k:
# fc = 1 / (2 * pi * 180e3 * 1e-6) = 1 / (2 * pi * 0.18) = 0.884 Hz
# If Cf = 1 uF and Rf = 18k:
# fc = 1 / (2 * pi * 18e3 * 1e-6) = 8.84 Hz

# Back calculation formula:
# |Av| = Ad * Rf / (Rf + Rin * (1 + Ad))
# Ad_back = |Av| * (Rf + Rin) / (Rf - |Av| * Rin)
def back_calc_Ad(Av_meas, Rf, Rin):
    return Av_meas * (Rf + Rin) / (Rf - Av_meas * Rin)

print("Back calculation for Gain 10 (Rf=180k, Rin=18k):")
# Notice: (Rf + Rin) / (Rf - Av * Rin) = (180 + 18) / (180 - Av * 18) = 198 / (180 - 18*Av) = 11 / (10 - Av)
# When Av = 7.52:
ad_b_752 = 7.52 * 198.0 / (180.0 - 7.52 * 18.0)
print(f"Av = 7.52: Ad_back = {ad_b_752:.2f}")

ad_b_770 = 7.70 * 198.0 / (180.0 - 7.70 * 18.0)
print(f"Av = 7.70: Ad_back = {ad_b_770:.2f}")

