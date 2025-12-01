import CoolProp.CoolProp as CP
import pandas as pd
import numpy as np
from funcoes.calc_comp import*

BTU_to_W = 0.293
kgh_to_kgs = 1/3600

def funcao_convergencia(df_compressor, T1, T3, liq_ref):
    
    # Calcular P1 e P2 para TODOS os pontos
    df_compressor['P1'] = df_compressor['T_evap_K'].apply(
        lambda T: CP.PropsSI('P', 'T', T, 'Q', 1, liq_ref)
    )
    df_compressor['P2'] = df_compressor['T_cond_K'].apply(
        lambda T: CP.PropsSI('P', 'T', T, 'Q', 0, liq_ref)
    )
    
    # Ajustar curva de massa (retorna array)
    m_array, m = ajuste_curva_massa(
        df_compressor['T_evap_K'].values, 
        df_compressor['P1'].values, 
        df_compressor['P2'].values, 
        df_compressor,
        T1,
        T3,
        liq_ref
    )
    
    # Ajustar curva de potência (retorna valores para o ponto específico)
    w, H2, _ = ajuste_curva_potencia(
        m_array,
        m,
        df_compressor['T_evap_K'].values, 
        df_compressor['P1'].values, 
        df_compressor['P2'].values, 
        df_compressor,
        T1,
        T3,
        liq_ref,
    )
    
    # Calcular para o ponto específico T1, T3
    S1 = CP.PropsSI('S', 'T', T1, 'Q', 1, liq_ref)
    P1_ponto = CP.PropsSI('P', 'T', T1, 'Q', 1, liq_ref)
    P3_ponto = CP.PropsSI('P', 'T', T3, 'Q', 0, liq_ref)
    H3 = CP.PropsSI('H', 'T', T3, 'Q', 0, liq_ref)
    
    QH = m * (H2 - H3)
    QL = QH - w
    
    return QL, m, w, H2, H3, S1, P1_ponto, P3_ponto



def funcao_padrao_real(compressor, liq_ref, T3, T1, estacao):

    df_compressor = pd.read_csv(f'Trab02\Compressores\{compressor}.csv', header=0, sep=';')
    df_compressor["capacidade"] = df_compressor["capacidade"]*BTU_to_W
    df_compressor["fluxo_massa"] = df_compressor["fluxo_massa"]*kgh_to_kgs

    QL_calc,m, w, H2, H3, S1, P1, P2 = funcao_convergencia(df_compressor, T1, T3, liq_ref)

    try:
        T2 = CP.PropsSI('T', 'H', H2, 'S', S1, liq_ref)

    except:
        T2=np.nan

    QH = QL_calc + w

    match estacao:
        case "verao":
            COP = QL_calc / w
            
        case "inverno":
            COP = QH / w
    

    

    H1 = CP.PropsSI('H', 'T', T1, 'S', S1, liq_ref)

    S2 = S1

    S3 = CP.PropsSI('S', 'T', T3, 'Q', 0, liq_ref)
    P3 = CP.PropsSI('P', 'T', T3, 'Q', 0, liq_ref)

    T4 = T1
    S4 = S3
    H4 = H3
    P4 = P1

    df_ciclo_real = pd.DataFrame({
        'Entrada': ['Compressor', 'Condensador', 'Capilar', 'Evaporador'],
        'T': [T1, T2, T3, T4],
        'P': [P1, P2, P3, P4],
        'H': [H1, H2, H3, H4],
        'S': [S1, S2, S3, S4],
        }, index=[1, 2, 3, 4] )

    real_dict={
        "compressor": compressor,
        "COP": COP,
        "QL": QL_calc,
        "QH": QH,
        "m": m,
        "w": QL_calc/COP,
        "df_ciclo": df_ciclo_real
    }

    return real_dict