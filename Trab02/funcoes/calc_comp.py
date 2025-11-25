import pandas as pd
import numpy as np
import CoolProp.CoolProp as CP
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


def ajuste_curva_massa(T1_array, P1_array, P2_array, df_compressor):
    """
    T1 = Ts (sucção)

    """
    
    N = 60 # Hz

    def funcao_massa(T1, b0, b1, b2):
        # Aqui T1 é um array, e precisamos dos P1 e P2 correspondentes
        m = (P1_array * N) / T1 * (b0 - b1 * (((P2_array / P1_array)**b2) - 1))
        return m
    
    params_massa, _ = curve_fit(
    funcao_massa, 
    df_compressor['T_evap_K'], 
    df_compressor['fluxo_massa'],
    p0=[1.0, 0.01, 0.3]  # Valores iniciais
    )

    b0, b1, b2 = params_massa
    m = funcao_massa(T1_array, b0, b1, b2)

    fig, ax = plt.subplots(figsize=(4, 8))


    ax.scatter(df_compressor['T_evap_K'], df_compressor['fluxo_massa'], color='r', marker='.')
    ax.plot(df_compressor['T_evap_K'], funcao_massa(df_compressor['T_evap_K'], *params_massa), '-b')
    
    df_verificação = pd.DataFrame()

    df_verificação['temp_exp'] = df_compressor['T_evap_K']
    df_verificação['pontos_exp'] = df_compressor['fluxo_massa']
    df_verificação['pontos_calc'] = funcao_massa(df_compressor['T_evap_K'], *params_massa)


    ax.set_xlabel("Temperatura de evaporação")
    ax.set_ylabel("Fluxo de massa")

    plt.tight_layout()
    plt.show()

    return m



def ajuste_curva_potencia(m_array, T1_array, P1_array, P2_array, df_compressor, liq_ref):
    """
    T1_array = Temperaturas de sucção (array)
    m_array = Fluxos de massa correspondentes (array)
    P1_array, P2_array = Pressões correspondentes (arrays)
    """
    
    def funcao_potencia(T1, a0, a1, a2):
        # Todos são arrays agora
        w = m_array * (a0*T1* ((P2_array/P1_array)**a1 - 1) + a2)
        return w
    
    params_potencia, _ = curve_fit(
        funcao_potencia, 
        df_compressor['T_evap_K'], 
        df_compressor['consumo'],  # ← Presumo que seja 'consumo', não 'capacidade'?
        p0=[0.001, 0.3, 100]  # Valores iniciais
    )
    
    a0, a1, a2 = params_potencia
    
    # Para calcular w e H2 em um ponto específico
    w_ponto = m_array[0] * (a0*T1_array[0]* ((P2_array[0]/P1_array[0])**a1 - 1) + a2)
    H1_ponto = CP.PropsSI('H', 'T', T1_array[0], 'Q', 1, liq_ref)
    H2_ponto = H1_ponto + w_ponto/m_array[0] + a2*10**-3
    
    # Plot
    fig, ax = plt.subplots(figsize=(4, 8))
    ax.scatter(df_compressor['T_evap_K'], df_compressor['consumo'], 
               color='r', marker='.', label='Experimental')
    ax.plot(df_compressor['T_evap_K'], 
            funcao_potencia(df_compressor['T_evap_K'], *params_potencia), 
            '-b', label='Ajustado')
    ax.set_xlabel("Temperatura de evaporação [K]")
    ax.set_ylabel("Potência [W]")
    ax.legend()
    plt.tight_layout()
    plt.show()
    
    return w_ponto, H2_ponto, params_potencia