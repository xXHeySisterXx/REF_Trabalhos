import pandas as pd
import numpy as np
import CoolProp.CoolProp as CP

def domo_refrigerante(liq_ref):

    T_min = CP.PropsSI('Tmin', liq_ref)
    T_max = CP.PropsSI('Tcrit', liq_ref)

    valores_T = np.linspace(T_min, T_max, 2000) # Liquido Saturado
    valores_H = []
    valores_P = []
    valores_S = []


    for T in valores_T:
        valores_H.append(CP.PropsSI('H', 'T', T, 'Q', 0, liq_ref))
        valores_P.append(CP.PropsSI('P', 'T', T, 'Q', 0, liq_ref))
        valores_S.append(CP.PropsSI('S', 'T', T, 'Q', 0, liq_ref))

    valores_T_invertida = np.flip(valores_T)

    for T in valores_T_invertida:
            valores_H.append(CP.PropsSI('H', 'T', T, 'Q', 1, liq_ref))
            valores_P.append(CP.PropsSI('P', 'T', T, 'Q', 1, liq_ref))
            valores_S.append(CP.PropsSI('S', 'T', T, 'Q', 1, liq_ref))

    valores_T_total = np.concatenate([valores_T, valores_T_invertida])
            
    df_domo = pd.DataFrame({
        'H': np.array(valores_H) / 1000,
        'P': np.array(valores_P) / 1000,
        'T': np.array(valores_T_total),
        'S': np.array(valores_S) / 1000,
    })

    return df_domo