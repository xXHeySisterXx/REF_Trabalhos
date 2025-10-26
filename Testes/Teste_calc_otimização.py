from scipy.optimize import minimize
import numpy as np
import CoolProp.CoolProp as CP
from scipy.optimize import brentq
from calc_auxiliar import*
from calc_COP import*
import pandas as pd
import numpy as np

def funcao_objetivo(T_vars, QL_desejado, df_compressor):
    """
    T_vars = [T1, T3]
    Retorna: erro quadrático entre QL_calculado e QL_desejado
    """
    T1, T3 = T_vars
    
    # Limites físicos
    if T1 >= T3:  # Evaporador deve ser mais frio que condensador
        return 1e10
    
    try:
        # Calcular QL para este par (T1, T3)
        P1 = CP.PropsSI('P', 'T', T1, 'Q', 1, "R134a")
        P3 = CP.PropsSI('P', 'T', T3, 'Q', 0, "R134a")
        P2 = P3
        
        m = ajuste_curva_massa(T1, P1, P2, df_compressor)
        w, H2 = ajuste_curva_potencia(m, T1, P1, P2, df_compressor)
        
        H3 = CP.PropsSI('H', 'T', T3, 'Q', 0, "R134a")
        QH = m * (H2 - H3)
        QL_calc = QH - w
        
        # Erro quadrático
        erro = (QL_calc - QL_desejado)**2
        
        return erro
    
    except:
        return 1e10  # Penalidade alta para pontos inválidos


def otimizar_ciclo(QL_desejado, compressor, T1_inicial=245, T3_inicial=315):
    """
    Encontra T1 e T3 ótimos que resultam no QL desejado
    """
    df_compressor = pd.read_csv(f'Trab01\programa\dados_compressores\{compressor}.csv', header=0, sep=',')

    
    # Chute inicial [T1, T3]
    x0 = [T1_inicial, T3_inicial]  # Ex: -20°C, 40°C
    
    # Limites (em Kelvin)
    bounds = [
        (233, 283),  # T1: -40°C a 10°C
        (293, 333)   # T3: 20°C a 60°C
    ]
    
    # Otimização
    resultado = minimize(
        funcao_objetivo,
        x0,
        args=(QL_desejado, df_compressor),
        method='L-BFGS-B',  # ou 'SLSQP', 'Nelder-Mead'
        bounds=bounds,
        options={'maxiter': 100}
    )
    
    if resultado.success:
        T1_otimo, T3_otimo = resultado.x
        print(f"✅ Convergiu!")
        print(f"T1 ótimo = {T1_otimo-273.15:.2f}°C")
        print(f"T3 ótimo = {T3_otimo-273.15:.2f}°C")
        print(f"Erro final = {np.sqrt(resultado.fun):.2f} W")
        
        # Calcular todos os parâmetros com valores ótimos
        serie_ciclo = calcular_ciclo_completo(T1_otimo, T3_otimo, df_compressor)
        return serie_ciclo
    else:
        print("❌ Não convergiu!")
        return None


def calcular_ciclo_completo(T1, T3, df_compressor):
    """Calcula todas as propriedades do ciclo para T1 e T3 dados"""
    try:
        S1 = CP.PropsSI('S', 'T', T1, 'Q', 1, "R134a")
        P1 = CP.PropsSI('P', 'T', T1, 'Q', 1, "R134a")
        P3 = CP.PropsSI('P', 'T', T3, 'Q', 0, "R134a")
        P2 = P3
        
        m = ajuste_curva_massa(T1, P1, P2, df_compressor)
        w, H2 = ajuste_curva_potencia(m, T1, P1, P2, df_compressor)
        H3 = CP.PropsSI('H', 'T', T3, 'Q', 0, "R134a")
        
        QH = m * (H2 - H3)
        QL = QH - w
        COP = QL/w
        
        # Tentativa mais robusta de calcular T2
        T2 = np.nan
        try:
            # Primeiro verifica se o ponto é fisicamente possível
            P_sat_H2 = CP.PropsSI('P', 'H', H2, 'S', S1, "R134a")
            
            # Se a pressão calculada for próxima de P2, o ponto é válido
            if abs(P_sat_H2 - P2) < P2 * 0.1:  # tolerância de 10%
                T2 = CP.PropsSI('T', 'H', H2, 'P', P2, "R134a")
            else:
                # Usa propriedades na pressão de descarga
                T2 = CP.PropsSI('T', 'H', H2, 'P', P2, "R134a")
        except:
            try:
                # Fallback: calcula T2 usando apenas H2 e P2
                T2 = CP.PropsSI('T', 'H', H2, 'P', P2, "R134a")
            except:
                print(f"⚠️  Não foi possível calcular T2. H2={H2:.2f}, P2={P2:.2f}")
                T2 = np.nan
        
        serie = pd.Series({
            'T1': T1, 'T2': T2, 'T3': T3,
            'P1': P1, 'P2': P2, 'P3': P3,
            'H2': H2, 'H3': H3,
            'S1': S1,
            'm': m, 'w': w,
            'QL': QL, 'QH': QH,
            'COP': COP
        })
        
        return serie
        
    except Exception as e:
        print(f"❌ Erro em calcular_ciclo_completo: {e}")
        return None


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

# Uso:
serie_otima = otimizar_ciclo(QL_desejado=81, compressor='EMI45HER')

df_ciclo_otimo = pontos_ciclo(serie_otima, "R134a")
plot_ciclo(df_ciclo_otimo, 'R134a')

# convergiu: EMU45HER e EMI45HER