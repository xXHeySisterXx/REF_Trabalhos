import CoolProp.CoolProp as CP
from scipy.optimize import brentq
from calc_COP import*
import pandas as pd
import numpy as np

def ciclo_padrao (T_amb, T_int, QL, liq_refrigerante):
    """
    # Ciclo Padrão de Carnot:

    Parâmetros conhecidos:

    :param QL: Taxa de resfriamento necessário
    :param T_amb: Temperatura ambiente
    :param T_int: Temperatura do interior do refrigerador

    Assumindo:
    T4 = T1
    S2 = S1
    P4 = P1
    T3 = T2
    P3 = P2
    H4 = H3
    S4 = S3

    """

    print(ciclo_padrao.__doc__)
    
    COP = calc_COP_temps(T_amb, T_int)
    W_compressor = QL/COP # W
    
    T1=T4=T_int
    T2=T3=T_amb

    S2 = CP.PropsSI('S', 'T', T2, 'Q', 1, liq_refrigerante) # [J/kgK]
    H2 = CP.PropsSI('H', 'T', T2, 'Q', 1, liq_refrigerante)  # [J/kg]
    P2 = CP.PropsSI('P', 'T', T2, 'Q', 1, liq_refrigerante)  # [Pa]

    S1=S2 # [J/kgK]
    H1 = CP.PropsSI('H', 'T', T1, 'S', S1, liq_refrigerante) # [J/kg]
    P1 = CP.PropsSI('P', 'T', T1, 'S', S1, liq_refrigerante) # [P]

    S3 = CP.PropsSI('S', 'T', T3, 'Q', 0, liq_refrigerante) # [J/kgK]
    H3 = CP.PropsSI('H', 'T', T3, 'Q', 0, liq_refrigerante)  # [J/kg]
    P3 = CP.PropsSI('P', 'T', T3, 'Q', 0, liq_refrigerante)  # [Pa]

    S4= CP.PropsSI('S', 'H', H3, 'T', T1, liq_refrigerante) # [J/kgK]
    H4 = H3 # [J/kg]
    P4 = CP.PropsSI('P', 'T', T4, 'S', S4, liq_refrigerante) # [P]

    fluxo_m = W_compressor/ (H2 - H1) # [kg/s]

    df_ciclo_padrao = pd.DataFrame({
        'Entrada': ['Compressor', 'Condensador', 'Capilar', 'Evaporador', 'Retorno'],
        'T': [T1, T2, T3, T4, T1],
        'P': [P1, P2, P3, P4, P1],
        'H': [H1, H2, H3, H4, H1],
        'S': [S1, S2, S3, S4, S1],
        'COP': [COP, np.nan, np.nan, np.nan, np.nan],
        'W': [W_compressor, np.nan, np.nan, np.nan, np.nan],
        'm': [fluxo_m, np.nan, np.nan, np.nan, np.nan],
        }, index=[1, 2, 3, 4, 5] )
    
    print(df_ciclo_padrao.head(6))

    return df_ciclo_padrao