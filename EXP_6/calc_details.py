import numpy as np

Ad = 35.83

# Unity gain:
Rf_u = 10e3
Rin_u = 10e3
beta_u = Rin_u / (Rf_u + Rin_u)
T_u = Ad * beta_u
Av_ideal_u = - Rf_u / Rin_u
Av_pred_u = - Ad * Rf_u / (Rf_u + Rin_u * (1 + Ad))

# Gain 10:
Rf_10 = 10e3
Rin_10 = 1e3
beta_10 = Rin_10 / (Rf_10 + Rin_10)
T_10 = Ad * beta_10
Av_ideal_10 = - Rf_10 / Rin_10
Av_pred_10 = - Ad * Rf_10 / (Rf_10 + Rin_10 * (1 + Ad))

print(f"Unity Gain: beta = {beta_u:.4f}, T = {T_u:.4f}, Ideal = {Av_ideal_u:.2f}, Predicted = {Av_pred_u:.4f}")
print(f"Gain 10:    beta = {beta_10:.4f}, T = {T_10:.4f}, Ideal = {Av_ideal_10:.2f}, Predicted = {Av_pred_10:.4f}")

# Back-calculate Ad from measured:
# Av_meas = - Ad_back * Rf / (Rf + Rin * (1 + Ad_back))
# |Av_meas| * (Rf + Rin + Rin * Ad_back) = Ad_back * Rf
# |Av_meas| * (Rf + Rin) + |Av_meas| * Rin * Ad_back = Ad_back * Rf
# Ad_back * (Rf - |Av_meas| * Rin) = |Av_meas| * (Rf + Rin)
# Ad_back = |Av_meas| * (Rf + Rin) / (Rf - |Av_meas| * Rin)

def back_calc_Ad(Av_meas, Rf, Rin):
    num = Av_meas * (Rf + Rin)
    den = Rf - Av_meas * Rin
    if den == 0:
        return np.inf
    return num / den

# For unity gain:
Av_meas_u = 1.000 # at 300mV, 400mV, 500mV, 1kHz
# Note: if Av_meas_u == 1.0, and Rf=10k, Rin=10k, den = 10k - 1.0*10k = 0 -> Ad_back -> infinity!
# But at 150mV: Av_meas_u = 1.087 (slightly > 1 due to measurement tolerance)
# At Vin = 50mV: Av_meas_u = 1.280
# If Av_meas_u = 0.99 or 0.947:
print("Back-calculated Ad for unity gain:")
for av in [0.947, 0.98, 0.99, 1.00]:
    print(f"Av = {av}: Ad_back = {back_calc_Ad(av, Rf_u, Rin_u):.2f}")

# For Gain 10:
print("\nBack-calculated Ad for gain of 10:")
# Measured gain at 50mV: 7.52, at 100mV: 7.40, at 500Hz: 7.70, at 700Hz: 8.00
for av in [7.40, 7.52, 7.65, 7.70, 8.00]:
    print(f"Av = {av}: Ad_back = {back_calc_Ad(av, Rf_10, Rin_10):.2f}")

