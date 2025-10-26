import CoolProp.CoolProp as CP

dT1 = - 5
dT3 = + 5
m = 0.000792

T1 = -25 + 273
T3 = 35 + 273

Ql = 186 # W
Wcomp = 160 # W

Te = T1 + dT1
Tc = T3 + dT3

Qh=Ql + Wcomp

COP_r = Te / (Tc - Te)


S1 = 1757.719106
S2 = 1757.719106
S3 = 1213.239687
S4 = 1213.239687

Se = m*(S1 - S4) + Ql/(-30+273)

Sc = m*(S2 - S3) + Qh/(40+273)


We = Se*Te
Wc = Sc*Tc

print("S evaporador", Se)
print("S condensador", Sc)

print("S We", We)
print("S Wc", Wc)

Wcomp = 83

COP = () / ()