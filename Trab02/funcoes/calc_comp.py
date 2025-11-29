import pandas as pd
import numpy as np
import CoolProp.CoolProp as CP
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


def ajuste_curva_massa(T1_array, P1_array, P2_array, df_compressor, T1, T3, liq_ref):
    """
    T1 = Ts (sucção)

    """
    
    N = 60 # Hz

    def funcao_massa(T1_var, b0, b1, b2):
        # Aqui T1 é um array, e precisamos dos P1 e P2 correspondentes
        m = (P1_array * N) / T1_var * (b0 - b1 * (((P2_array / P1_array)**b2) - 1))
        return m
    

    P1 = CP.PropsSI('P', 'T', T1, 'Q', 1, liq_ref)
    P2 = CP.PropsSI('P', 'T', T3, 'Q', 0, liq_ref)
    
    def funcao_massa_ponto(T1, b0, b1, b2):
        # Aqui T1 é um array, e precisamos dos P1 e P2 correspondentes
        m = (P1 * N) / T1 * (b0 - b1 * (((P2 / P1)**b2) - 1))
        return m

    params_massa, _ = curve_fit(
    funcao_massa, 
    df_compressor['T_evap_K'], 
    df_compressor['fluxo_massa'],
    p0=[1.0, 0.01, 0.3]  # Valores iniciais
    )

    b0, b1, b2 = params_massa
    m_array = funcao_massa_ponto(T1_array, b0, b1, b2)
    m = funcao_massa_ponto(T1, b0, b1, b2)

    # fig, ax = plt.subplots(figsize=(4, 8))
    # ax.scatter(df_compressor['T_evap_K'], df_compressor['fluxo_massa'], color='r', marker='.')
    # ax.plot(df_compressor['T_evap_K'], funcao_massa(df_compressor['T_evap_K'], *params_massa), '-b')
    # ax.set_xlabel("Temperatura de evaporação")
    # ax.set_ylabel("Fluxo de massa")

    # plt.tight_layout()
    # plt.show()

    return m_array, m



def ajuste_curva_potencia(m_array, m, T1_array, P1_array, P2_array, df_compressor, T1, T3, liq_ref):
    """
    T1_array = Temperaturas de sucção (array)
    m_array = Fluxos de massa correspondentes (array)
    P1_array, P2_array = Pressões correspondentes (arrays)
    """
    
    m_exp = df_compressor['fluxo_massa'].values

    def funcao_potencia(T1_var, a0, a1, a2):
        # Todos são arrays agora
        w = m_exp * (a0*T1_var* ((P2_array/P1_array)**a1 - 1) + a2)
        return w
    
    P1 = CP.PropsSI('P', 'T', T1, 'Q', 1, liq_ref)
    P2 = CP.PropsSI('P', 'T', T3, 'Q', 0, liq_ref)
    
    def funcao_potencia_ponto(T1, a0, a1, a2):
        # Todos são arrays agora
        w = m * (a0*T1* ((P2/P1)**a1 - 1) + a2)
        return w
    
    params_potencia, _ = curve_fit(
        funcao_potencia, 
        df_compressor['T_evap_K'], 
        df_compressor['consumo'],  # ← Presumo que seja 'consumo', não 'capacidade'?
        p0=[0.001, 0.3, 100]  # Valores iniciais
    )
    
    a0, a1, a2 = params_potencia
    
    # Para calcular w e H2 em um ponto específico
    w_ponto = funcao_potencia_ponto(T1, a0, a1, a2)
    H1_ponto = CP.PropsSI('H', 'T', T1, 'Q', 1, liq_ref)
    H2_ponto = H1_ponto + w_ponto/m + a2*10**-3
    
    # # Plot
    # fig, ax = plt.subplots(figsize=(4, 8))
    # ax.scatter(df_compressor['T_evap_K'], df_compressor['consumo'], 
    #            color='r', marker='.', label='Experimental')
    # ax.plot(df_compressor['T_evap_K'], 
    #         funcao_potencia(df_compressor['T_evap_K'], *params_potencia), 
    #         '-b', label='Ajustado')
    # ax.set_xlabel("Temperatura de evaporação [K]")
    # ax.set_ylabel("Potência [W]")
    # ax.legend()
    # plt.tight_layout()
    # plt.show()
    
    return w_ponto, H2_ponto, params_potencia