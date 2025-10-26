import CoolProp.CoolProp as CP
from scipy.optimize import brentq
from calc_auxiliar import*
from calc_COP import*
import pandas as pd
import numpy as np


def funcao_convergencia(df_compressor_entrada, T1, T3):
    
    S1 = CP.PropsSI('S', 'T', T1, 'Q', 1, "R134a") # [J/kgK]
    P1 = CP.PropsSI('P', 'T', T1, 'Q', 1, "R134a") # [J/kgK]
    P3 = CP.PropsSI('P', 'T', T3, 'Q', 0, "R134a")  # [Pa]
    P2=P3

    m = ajuste_curva_massa(T1, P1, P2, df_compressor_entrada)
    w, H2 = ajuste_curva_potencia(m, T1, P1, P2, df_compressor_entrada)

    H3 = CP.PropsSI('H', 'T', T3, 'Q', 0, "R134a") # [J/kgK]
    QH = m*(H2-H3)
    QL = QH - w

    return QL, m, w, H2, H3, S1, P1, P3



def funcao_padrao_real(QL, T1i, compressor):

    print(QL)


    df_compressor_entrada=dataframe_compressor(compressor)
    Temps_condensador = sorted(df_compressor_entrada['T_condensador'].unique())

    
    QL_calc_valores = []
    diferenca_QL = []
    m_valores = []
    w_valores = []
    T1_valores = []
    T2_valores = []
    T3_valores = []
    H2_valores = []
    H3_valores = []
    S1_valores = []
    P1_valores = []
    P2_valores = []
    COP_valores = []

    for T3 in Temps_condensador:
        df_compressor = df_compressor_entrada[df_compressor_entrada['T_condensador']==T3].copy()
            
        for T1 in df_compressor['T_evaporador']: #! Tevap é T4 e T1, Tcond é T3

            
            QL_calc,m, w, H2, H3, S1, P1, P2 = funcao_convergencia(df_compressor, T1, T3)

            QL_calc_valores.append(QL_calc)
            diferenca_QL.append(QL_calc - QL)

            try:
                T2 = CP.PropsSI('T', 'H', H2, 'S', S1, "R134a")  # [Pa]

            except:
                T2=np.nan


            COP = QL_calc / w

            m_valores.append(m)
            w_valores.append(w)
            T1_valores.append(T1)
            T2_valores.append(T2)
            T3_valores.append(T3)
            H2_valores.append(H2)
            H3_valores.append(H3)
            S1_valores.append(S1)
            P1_valores.append(P1)
            P2_valores.append(P2)
            COP_valores.append(COP)


    df_resultados = pd.DataFrame({
        'm': np.array(m_valores),
        'w': np.array(w_valores),
        'T2': np.array(T2_valores),
        'T3': np.array(T3_valores),
        'T1': np.array(T1_valores),
        'QL': np.array(QL),
        'QL_c': np.array(QL_calc_valores),
        'QL_d': np.array(diferenca_QL),
        'COP': np.array(COP_valores),
        'H2': np.array(H2_valores),
        'H3': np.array(H3_valores),
        'S1': np.array(S1_valores),
        'P1': np.array(P1_valores),
        'P2': np.array(P2_valores),
    })

    df_resultados = df_resultados.sort_values(by='w').reset_index(drop=True)
    df_resultados_limpo = df_resultados[(df_resultados['QL_d'] >= 0) & (df_resultados['T2'] > 0)].copy()

    print("\ndf_resultados:")
    print(df_resultados.head(20))

    print("\ndf_resultados_limpo:")
    print(df_resultados_limpo.head(20))

    serie_ciclo_real = (df_resultados.iloc[0, :]).copy()

    return serie_ciclo_real






def pontos_ciclo(serie_ciclo_real, liq_refrigerante):

    T1 = serie_ciclo_real['T1']
    P1 = serie_ciclo_real['P1']
    S1 = serie_ciclo_real['S1']
    H1 = CP.PropsSI('H', 'T', T1, 'S', S1, liq_refrigerante)

    T2 = serie_ciclo_real['T2']
    P2 = serie_ciclo_real['P2']
    S2 = S1
    H2 = serie_ciclo_real['H2']

    H3 = serie_ciclo_real['H3']
    T3 = serie_ciclo_real['T3']
    S3 = CP.PropsSI('S', 'T', T3, 'Q', 0, liq_refrigerante)
    P3 = CP.PropsSI('P', 'T', T3, 'Q', 0, liq_refrigerante)

    T4 = T1
    S4 = S3
    H4 = H3
    P4 = P1

    COP = serie_ciclo_real['COP']

    df_ciclo_real = pd.DataFrame({
        'Entrada': ['Compressor', 'Condensador', 'Capilar', 'Evaporador', 'Retorno'],
        'T': [T1, T2, T3, T4, T1],
        'P': [P1, P2, P3, P4, P1],
        'H': [H1, H2, H3, H4, H1],
        'S': [S1, S2, S3, S4, S1],
        'COP': [COP, np.nan, np.nan, np.nan, np.nan],
        'W': [serie_ciclo_real['w'], np.nan, np.nan, np.nan, np.nan],
        'm': [serie_ciclo_real['m'], np.nan, np.nan, np.nan, np.nan],
        }, index=[1, 2, 3, 4, 5] )
    
    print("\ndf_ciclo_real:")
    print(df_ciclo_real.head(6))

    return df_ciclo_real


# Todo:
    # Plots e prints de diagnostico do estado atual
    # Revisar slides sobre compressores, será que não posso mais usar S1=S2? #! OK
    # Revisar dados compressores #! OK
    # pesquisar interpolação superfície e convergência de duas variáveis



# Chutar T1, calcular T2 para conseguir QL?