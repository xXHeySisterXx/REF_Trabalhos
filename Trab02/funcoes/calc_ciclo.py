import CoolProp.CoolProp as CP
import pandas as pd
import numpy as np
from funcoes.calc_comp import*

BTU_to_W = 0.293

def funcao_convergencia(df_compressor, T1, T3, liq_ref):
    
    S1 = CP.PropsSI('S', 'T', T1, 'Q', 1, liq_ref) # [J/kgK]
    P1 = CP.PropsSI('P', 'T', T1, 'Q', 1, liq_ref) # [J/kgK]
    P3 = CP.PropsSI('P', 'T', T3, 'Q', 0, liq_ref)  # [Pa]
    P2=P3

    m = ajuste_curva_massa(T1, P1, P2, df_compressor)
    w, H2 = ajuste_curva_potencia(m, T1, P1, P2, df_compressor)

    H3 = CP.PropsSI('H', 'T', T3, 'Q', 0, liq_ref) # [J/kgK]
    QH = m*(H2-H3)
    QL = QH - w

    return QL, m, w, H2, H3, S1, P1, P3



def funcao_padrao_real(QL, compressor, liq_ref):

    df_compressor = pd.read_csv(f'Trab02\Compressores\{compressor}.csv', header=0, sep=';')
    Temps_condensador = sorted(df_compressor['T_cond_K'].unique())
    df_compressor["capacidade"] = df_compressor["capacidade"]*BTU_to_W

    
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
        df_compressor = df_compressor[df_compressor['T_cond_K']==T3].copy()
            
        for T1 in df_compressor['T_evap_K']: #! Tevap é T4 e T1, Tcond é T3

            
            QL_calc,m, w, H2, H3, S1, P1, P2 = funcao_convergencia(df_compressor, T1, T3, liq_ref)

            QL_calc_valores.append(QL_calc)
            diferenca_QL.append(QL_calc - QL)

            try:
                T2 = CP.PropsSI('T', 'H', H2, 'S', S1, liq_ref)  # [Pa]

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