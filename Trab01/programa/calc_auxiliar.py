import pandas as pd
import numpy as np
import CoolProp.CoolProp as CP
import matplotlib.pyplot as plt



#? ================================= Quantidade de calor
def calc_Q(massa, calor, diff_temp=1):
    Q = massa*calor*diff_temp
    return Q


#? ================================= Domo fases liq
def domo_refrigerante(liq_refrigerante):

    T_min = CP.PropsSI('Tmin', liq_refrigerante)
    T_max = CP.PropsSI('Tcrit', liq_refrigerante)

    valores_T = np.linspace(T_min+1, T_max-1, 2000) # Liquido Saturado
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

    
    fig, (TS, PH) = plt.subplots(1, 2, figsize = (18, 6))

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
