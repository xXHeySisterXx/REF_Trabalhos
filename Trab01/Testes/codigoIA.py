from scipy.optimize import minimize
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
        S1 = CP.PropsSI('S', 'T', T1, 'Q', 1, "R134a")
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


def otimizar_ciclo(QL_desejado, compressor, T1_inicial=253, T3_inicial=313):
    """
    Encontra T1 e T3 ótimos que resultam no QL desejado
    """
    df_compressor = dataframe_compressor(compressor)
    
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
    S1 = CP.PropsSI('S', 'T', T1, 'Q', 1, "R134a")
    P1 = CP.PropsSI('P', 'T', T1, 'Q', 1, "R134a")
    P3 = CP.PropsSI('P', 'T', T3, 'Q', 0, "R134a")
    P2 = P3
    
    m = ajuste_curva_massa(T1, P1, P2, df_compressor)
    w, H2 = ajuste_curva_potencia(m, T1, P1, P2, df_compressor)
    H3 = CP.PropsSI('H', 'T', T3, 'Q', 0, "R134a")
    
    QH = m * (H2 - H3)
    QL = QH - w
    
    try:
        T2 = CP.PropsSI('T', 'H', H2, 'S', S1, "R134a")
    except:
        T2 = np.nan
    
    serie = pd.Series({
        'T1': T1, 'T2': T2, 'T3': T3,
        'P1': P1, 'P2': P2, 'P3': P3,
        'H2': H2, 'H3': H3,
        'S1': S1,
        'm': m, 'w': w,
        'QL': QL, 'QH': QH
    })
    
    return serie

# Uso:
serie_otima = otimizar_ciclo(QL_desejado=5000, compressor='seu_compressor')