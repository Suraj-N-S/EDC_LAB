import numpy as np
import openpyxl

# Ad = 35.83
Ad = 35.83

# Theory formula:
# Av = - Ad * Rf / (Rf + Rin * (1 + Ad))
# For Unity gain: Rf = 10k, Rin = 10k (or Rf/Rin = 1, Rf = 180k, Rin = 18k? Wait, what are Rf and Rin?)
# Let's check:
# In PDF:
# Section 2 & 9:
# Unity gain: Rf = 10 kOhm, Rin = 10 kOhm. beta = Rin/(Rf+Rin) = 0.5.
# If Ad = 35.83:
# Unity gain Av_calc = - 35.83 * 10 / (10 + 10*(1 + 35.83)) = - 35.83 / (1 + 1 + 35.83) = - 35.83 / 37.83 = - 0.9471 V/V.
# Gain of 10: Rf = 10 kOhm, Rin = 1 kOhm. beta = 1 / (10 + 1) = 1/11 = 0.090909.
# Gain-of-10 Av_calc = - 35.83 * 10 / (10 + 1 * (1 + 35.83)) = - 358.3 / (10 + 36.83) = - 358.3 / 46.83 = - 7.651 V/V.

# Wait, let's also check if Rf = 180k and Rin = 18k was unity or 10? In LTspice: R8=180k, R9=180k, R6=18k, R7=18k -> ratio is 10!
# What about unity in LTspice? R_in would be 180k or 18k with Rf=18k?

print(f"With Ad = {Ad}:")
print("If Rf=10k, Rin=10k:")
Av_unity = - Ad * 10.0 / (10.0 + 10.0 * (1 + Ad))
print(f"Unity Gain: {Av_unity:.4f}, |Av| = {abs(Av_unity):.4f}")

Av_10 = - Ad * 10.0 / (10.0 + 1.0 * (1 + Ad))
print(f"Gain 10 (Rf=10k, Rin=1k): {Av_10:.4f}, |Av| = {abs(Av_10):.4f}")

# What if ratio is Rf/Rin = 10 (e.g. 180k/18k):
Av_10_alt = - Ad * 180.0 / (180.0 + 18.0 * (1 + Ad))
print(f"Gain 10 (Rf=180k, Rin=18k): {Av_10_alt:.4f}, |Av| = {abs(Av_10_alt):.4f}")

