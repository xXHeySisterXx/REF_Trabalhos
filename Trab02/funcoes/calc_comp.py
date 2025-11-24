import pandas as pd
import numpy as np
import CoolProp.CoolProp as CP
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


def ajuste_curva_massa(T1, P1, P2, df_compressor):
    """
    T1 = Ts (sucção)

    """
    
    N = 60 # Hz

    def funcao_massa(T1, b0, b1, b2):
        m = (P1*N)/T1 * (b0 - b1 * (( (P2/P1)**b2) - 1 ))
        return m
    
    params_massa, _ = curve_fit(funcao_massa, df_compressor['T_evaporador'], df_compressor['fluxo_massa']/(60*60))
    b0, b1, b2 = params_massa
    m = funcao_massa(T1, b0, b1, b2)

    # fig, (ax) = plt.subplots(figsize = (4,8))

    # ax.plot(df_compressor['T_evaporador'], df_compressor['fluxo_massa'], color = 'r', marker = '.')
    # ax.plot(df_compressor['T_evaporador'], funcao_massa(df_compressor['T_evaporador'], *params_massa), '-b')

    # plt.legend()
    # plt.tight_layout()
    # plt.show()

    return m



def ajuste_curva_potencia(m, T1, P1, P2, df_compressor):
    """
    T1 = Ts (sucção)

    """

    def funcao_potencia(T1, a0, a1, a2, liq_ref):
        w = m* ( a0*T1* ((P2/P1)**a1 - 1) + a2)
        return w

    params_potencia, _ = curve_fit(funcao_potencia, df_compressor['T_evaporador'], df_compressor['capacidade'])
    a0, a1, a2 = params_potencia
    w = funcao_potencia(T1, a0, a1, a2)

    H1 = CP.PropsSI('H', 'T', T1, 'Q', 1, liq_ref) # [J/kgK]
    H2 = H1 + w/m + a2*10**-3

    # fig, (ax) = plt.subplots(figsize = (4,8))

    # ax.plot(df_compressor['T_evaporador'], df_compressor['capacidade'], color = 'r', marker = '.')
    # ax.plot(df_compressor['T_evaporador'], funcao_potencia(df_compressor['T_evaporador'], *params_potencia), '-b')

    # plt.legend()
    # plt.tight_layout()
    # plt.show()


    return w, H2