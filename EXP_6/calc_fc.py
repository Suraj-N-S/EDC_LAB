import numpy as np

# Cutoff frequencies:
# For Unity Gain:
# Rin = 18k, Cin = 1 uF
# Rf = 18k, Cf = 1 uF
fc_in_u = 1.0 / (2 * np.pi * 18e3 * 1e-6)
fc_f_u = 1.0 / (2 * np.pi * 18e3 * 1e-6)
print(f"Unity Gain: fc_in = {fc_in_u:.2f} Hz, fc_f = {fc_f_u:.2f} Hz")

# For Gain of 10:
# Rin = 18k, Cin = 10 uF
# Rf = 180k, Cf = 1 uF
fc_in_10 = 1.0 / (2 * np.pi * 18e3 * 10e-6)
fc_f_10 = 1.0 / (2 * np.pi * 180e3 * 1e-6)
print(f"Gain of 10: fc_in = {fc_in_10:.2f} Hz, fc_f = {fc_f_10:.2f} Hz")

