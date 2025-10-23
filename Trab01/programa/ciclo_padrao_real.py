import CoolProp.CoolProp as CP
from scipy.optimize import brentq
from calc_auxiliar import*
import pandas as pd
import numpy as np


def funcao_convergencia(df_compressor_entrada, T1, T2):

    S1 = CP.PropsSI('S', 'T', T1, 'Q', 1, "R134a") # [J/kgK]
    P1 = CP.PropsSI('P', 'T', T1, 'Q', 1, "R134a") # [J/kgK]
    P2 = CP.PropsSI('P', 'T', T2, 'S', S1, "R134a")  # [Pa]

    m = ajuste_curva_massa(T1, T2, P1, P2, df_compressor_entrada)
    w, H2 = ajuste_curva_potencia(m, T1, T2, P1, P2, df_compressor_entrada)

    H3 = CP.PropsSI('H', 'T', T1, 'Q', 0, "R134a") # [J/kgK]
    QH = m*(H2-H3)
    QL = QH - w

    return QL


#! T1 pode ser menor que -25°C e T2 maior que 35°C
#! QL é o critério de convergência

def funcao_padrao_real(QL, T1i, T2i, compressor):

    df_compressor_entrada=dataframe_compressor(compressor)

    def calc_Te_Tc(T1, T2):
        
        funcao_convergencia(df_compressor_entrada, T1, T2)
    




    calc_Te_Tc(T1 = T1i, T2 = T2i)

    return



funcao_padrao_real(81, -25 + 273, 35 + 273, "EMI40HNR")