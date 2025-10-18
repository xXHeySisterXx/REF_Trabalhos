import CoolProp.CoolProp as CP
from calc_COP import*

def ciclo_padrao (T_amb, T_int, QL, fluxo_m):
    """
    # Essa

    T_amb Temperatura em Kelvin
    """
    COP = calc_COP_temps(T_amb, T_int)
    W_compressor = QL/COP # kW

    T1=T_int
    T2=W_compressor/fluxo_m+T1  # Todo T1 é uma temperatura iterável


    """
    T4 = T1
    S2 = S1
    P4 = P1
    T3 = T2
    P3 = P2
    H4 = H3
    S4 = S3
    """

    return
