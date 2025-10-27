import CoolProp.CoolProp as CP
from scipy.optimize import brentq
import pandas as pd
import numpy as np

# Pro compressor EMI40HNR , calculado a partir do rated points disponiveis

T_evap = -23.3 +273

T_cond  = 53.4 + 273

fluid = "R134a"


S1 = p1 = CP.PropsSI('S', 'T', T_evap, 'Q', 1, fluid)

#? Em 2

# s2 = CP.PropsSI('S', 'T', T_cond, 'Q', 1, fluid)
p2 = CP.PropsSI('P', 'T', T_cond, 'S', S1, fluid)


#? Em 1
# s1 = s2
# #p1 = CP.PropsSI('P', 'T', T_evap, 'S', s1, fluid)
p1 = CP.PropsSI('P', 'T', T_evap, 'Q', 1, fluid) # já considerando um superaquicimento, ambos são vapor 

razao_comp = p2/p1

print("A razão de compressão é :", razao_comp)