import pandas as pd
import numpy as np
import CoolProp.CoolProp as CP
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit



#? ================================= Quantidade de calor
def calc_Q(massa, calor, diff_temp=1):
    Q = massa*calor*diff_temp
    return Q


#? ================================= Domo fases liq
def domo_refrigerante(liq_refrigerante):

    T_min = CP.PropsSI('Tmin', liq_refrigerante)
    T_max = CP.PropsSI('Tcrit', liq_refrigerante)

    valores_T = np.linspace(T_min, T_max, 2000) # Liquido Saturado
    valores_H = []
    valores_P = []
    valores_S = []


    for T in valores_T:
        valores_H.append(CP.PropsSI('H', 'T', T, 'Q', 0, liq_refrigerante))
        valores_P.append(CP.PropsSI('P', 'T', T, 'Q', 0, liq_refrigerante))
        valores_S.append(CP.PropsSI('S', 'T', T, 'Q', 0, liq_refrigerante))

    valores_T_invertida = np.flip(valores_T)

    for T in valores_T_invertida:
            valores_H.append(CP.PropsSI('H', 'T', T, 'Q', 1, liq_refrigerante))
            valores_P.append(CP.PropsSI('P', 'T', T, 'Q', 1, liq_refrigerante))
            valores_S.append(CP.PropsSI('S', 'T', T, 'Q', 1, liq_refrigerante))

    valores_T_total = np.concatenate([valores_T, valores_T_invertida])
            
    df_domo = pd.DataFrame({
        'H': np.array(valores_H) / 1000,
        'P': np.array(valores_P) / 1000,
        'T': np.array(valores_T_total),
        'S': np.array(valores_S) / 1000,
    })

    return df_domo

def plot_ciclo (df_cliclo, liq_refrigerante):
    df_domo = domo_refrigerante(liq_refrigerante)

    
    fig, (TS, PH) = plt.subplots(1, 2, figsize = (12, 3))

    TS.plot(df_domo['S'], df_domo['T'])
    PH.plot(df_domo['H'], df_domo['P'])
    TS.plot(df_cliclo['S']/1000, df_cliclo['T'])
    PH.plot(df_cliclo['H']/1000, df_cliclo['P']/1000)

    plt.title(f'Ciclo com {liq_refrigerante}', fontsize=13, fontweight='bold')

    TS.set_xlabel("Entropia [kJ/kgK]")
    TS.set_ylabel("Temperatura [K]")

    PH.set_xlabel("Entalpia [kJ/kg]")
    PH.set_ylabel("Pressão [kPa]")

    plt.tight_layout()
    plt.show()

    return


def ajuste_curva(funcao_desejada, T1, T2, P1, P2):
    """
    T1 = Ts (sucção)

    """
    df_compressores = pd.DataFrame({
        'T_condensador':[1],
        'T_evaporador': [1],
        'capacidade': [1],
        'eficiencia': [1],
        'fluxo_massa': [1]
        })
    
    N = 60
    if (funcao_desejada=='massa'):
         m = P2*N/T2*(b0 - b1 ( (P2/P1)** b2 - 1 ))
    elif (funcao_desejada=='potencia'):
         w = m*( a0*T2*((P2/P1)**a1 -1) + a2)

    
   


                   
                   

        
        
    x = np.linspace(0, 10, 100)
    y_alvo = funcao_compressor

    params, _ = curve_fit(funcao_compressor, a0, a1, a2, y_alvo, )