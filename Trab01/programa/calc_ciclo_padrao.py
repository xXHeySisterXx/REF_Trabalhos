import CoolProp.CoolProp as CP
from calc_COP import*
"""
T cond com 10 de superaquecimento em relação a T_amb
T evap com 10 de subresfriamento em relação a T_int 

"""


def ciclo_padrao (T_amb, T_int, QL, fluxo_m):
    COP = calc_COP_temps(T_amb, T_int)
    W_comp = QL/COP

    T1=T_int
    T2=W_comp/fluxo_m+T1

    T1 = T_int - 10

    T2 = T_amb + 10         # K
    P2 = CP.PropsSI('P', 'T', T2 , 'Q', 1, 'R407C') # Pa 

    T3 = T2
    P3 = P2
    S3 = CP.PropsSI('S', 'T', T3 , 'P', P3, 'R134a')

    # P4 = CP.PropsSI('P', 'S', S3 , 'T', T1, 'R407C')

    print(S3/1000)




    return



# T1
# P1
# h1
# s1

# T2
# P2
# h2
# s2

# T3
# P3
# h3
# s3

# T4
# P4
# h4
# s4