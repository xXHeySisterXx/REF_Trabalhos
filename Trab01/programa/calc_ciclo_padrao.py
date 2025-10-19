import CoolProp.CoolProp as CP
from scipy.optimize import brentq
from calc_COP import*
import pandas as pd

def ciclo_padrao (T_amb, T_int, QL):
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

    print("COP = ", COP)
    print("W_compressor = ", W_compressor)

    
    T1=T4=T_int
    T2=T3=T_amb

    S2 = CP.PropsSI('S', 'T', T2, 'Q', 1, 'R134a') # [J/kgK]
    H2 = CP.PropsSI('H', 'T', T2, 'Q', 1, 'R134a')  # [J/kg]
    P2 = CP.PropsSI('P', 'T', T2, 'Q', 1, 'R134a')  # [Pa]

    S1=S2 # [J/kgK]
    H1 = CP.PropsSI('H', 'T', T1, 'S', S1, 'R134a') # [J/kg]
    P1 = CP.PropsSI('P', 'T', T1, 'S', S1, 'R134a') # [P]

    S3 = CP.PropsSI('S', 'T', T3, 'Q', 0, 'R134a') # [J/kgK]
    H3 = CP.PropsSI('H', 'T', T3, 'Q', 0, 'R134a')  # [J/kg]
    P3 = CP.PropsSI('P', 'T', T3, 'Q', 0, 'R134a')  # [Pa]

    S4=S3 # [J/kgK]
    H4 = H3 # [J/kg]
    P4 = CP.PropsSI('P', 'T', T4, 'S', S4, 'R134a') # [P]

    fluxo_m = W_compressor/ (H2 - H1) # [kg/s]

    df_ciclo_padrao = pd.DataFrame({
        'Entrada': ['Compressor', 'Condensador', 'Capilar', 'Evaporador'],
        'T_em_K': [T1, T2, T3, T4],
        "P_em_Pa": [P1, P2, P3, P4],
        'H_em_J': [H1, H2, H3, H4],
        'S_em_J': [S1, S2, S3, S4]
        }, index=[1, 2, 3, 4] )

    print(df_ciclo_padrao.head(5))

    # Todo Printar com o domo de transformação
    # todo Tornar o Fluido uma variável

    return