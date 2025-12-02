"""
BOMBA DE CALOR - Cálculo Simplificado
Objetivo: Q_condensador > 4950 W
"""

import CoolProp.CoolProp as CP
import pandas as pd


def calc_inverno(liq_ref):
    # ===== DADOS DE ENTRADA =====
    UA_cond = 1416.68   # W/K - Coeficiente condensador
    UA_evap = 1083.21   # W/K - Coeficiente evaporador
    W_comp = 1667.35    # W - Trabalho do compressor
    T_ext = 9           # °C - Temperatura externa (fria)
    T_int = 18          # °C - Temperatura interna (a aquecer)

    print("=" * 60)
    print("BOMBA DE CALOR - Cálculo Simplificado")
    print("=" * 60)
    print(f"\nDados:")
    print(f"  UA_condensador = {UA_cond} W/K")
    print(f"  UA_evaporador = {UA_evap} W/K")
    print(f"  W_compressor = {W_comp} W")
    print(f"  T_externa = {T_ext} °C")
    print(f"  T_interna = {T_int} °C")


    # ===== MÉTODO ITERATIVO SIMPLES =====
    print("\n" + "=" * 60)
    print("CÁLCULO ITERATIVO")
    print("=" * 60)

    # Chutes iniciais
    T_cond = T_int +2.4    # Condensador um pouco acima da temperatura interna
    T_evap = T_ext -2.7  # Evaporador um pouco abaixo da temperatura externa

    # Iteração
    for i in range(100):
        # Passo 1: Calcula Q_evap com T_evap atual
        Q_evap = UA_evap * (T_ext - T_evap)
        
        # Passo 2: Pelo balanço de energia: Q_cond = Q_evap + W_comp
        Q_cond_necessario = Q_evap + W_comp
        
        # Passo 3: Calcula T_cond necessário
        T_cond_novo = T_int + Q_cond_necessario / UA_cond
        
        # Passo 4: Recalcula Q_cond com novo T_cond
        Q_cond = UA_cond * (T_cond_novo - T_int)
        
        # Passo 5: Recalcula Q_evap pelo balanço
        Q_evap_novo = Q_cond - W_comp
        
        # Passo 6: Calcula T_evap necessário
        T_evap_novo = T_ext - Q_evap_novo / UA_evap
        
        # Verifica convergência
        erro_cond = abs(T_cond_novo - T_cond)
        erro_evap = abs(T_evap_novo - T_evap)
        
        # Atualiza temperaturas
        T_cond = T_cond_novo
        T_evap = T_evap_novo
        
        # Para quando convergir
        if erro_cond < 1e-10 and erro_evap < 1e-10 and (Q_cond > 4395):
            print(f"\nConvergiu em {i+1} iterações")
            break
        else: print("não convergiu")


    # ===== RESULTADOS FINAIS =====
    print("\n" + "=" * 60)
    print("RESULTADOS")
    print("=" * 60)

    # Calcula os calores finais
    Q_cond = UA_cond * (T_cond - T_int)
    Q_evap = UA_evap * (T_ext - T_evap)

    print(f"\nTemperaturas:")
    print(f"  T_condensador = {T_cond:.2f} °C")
    print(f"  T_evaporador = {T_evap:.2f} °C")
    print(f"  Diferença (ΔT) = {T_cond - T_evap:.2f} °C")

    print(f"\nCalores:")
    print(f"  Q_condensador (calor emitido) = {Q_cond:.2f} W")
    print(f"  Q_evaporador (calor absorvido) = {Q_evap:.2f} W")
    print(f"  W_compressor = {W_comp:.2f} W")

    print(f"\nVerificação do balanço:")
    erro_balanco = abs(Q_cond - Q_evap - W_comp)
    print(f"  Q_cond - (Q_evap + W_comp) = {erro_balanco:.4f} W")
    if erro_balanco < 0.01:
        print("  ✓ Balanço OK!")
    else:
        print("  ✗ Erro no balanço!")

    print(f"\nEficiência:")
    COP = Q_cond / W_comp
    print(f"  COP = {COP:.2f}")
    print(f"  Para cada 1 W consumido, fornece {COP:.2f} W de calor")


    # ===== VERIFICAÇÃO DO OBJETIVO =====
    print("\n" + "=" * 60)
    print("VERIFICAÇÃO DO OBJETIVO")
    print("=" * 60)
    objetivo = 4395
    print(f"  Objetivo: Q_condensador > {objetivo} W")
    print(f"  Atual: Q_condensador = {Q_cond:.2f} W")

    if Q_cond > objetivo:
        print(f"  ✓ OBJETIVO ATINGIDO! ({Q_cond - objetivo:.2f} W acima)")
    else:
        print(f"  ✗ Objetivo não atingido (faltam {objetivo - Q_cond:.2f} W)")
        print(f"\n  Para atingir {objetivo} W, você pode:")
        print(f"    • Aumentar UA_condensador")
        print(f"    • Aumentar W_compressor")
        print(f"    • Aumentar UA_evaporador")


    # ===== DETALHAMENTO DAS EQUAÇÕES =====
    print("\n" + "=" * 60)
    print("DETALHAMENTO DAS EQUAÇÕES USADAS")
    print("=" * 60)
    print("\n1. Calor no condensador (aquece o ambiente):")
    print(f"   Q_cond = UA_cond × (T_cond - T_int)")
    print(f"   Q_cond = {UA_cond} × ({T_cond:.2f} - {T_int})")
    print(f"   Q_cond = {Q_cond:.2f} W")

    print("\n2. Calor no evaporador (absorve do exterior):")
    print(f"   Q_evap = UA_evap × (T_ext - T_evap)")
    print(f"   Q_evap = {UA_evap} × ({T_ext} - {T_evap:.2f})")
    print(f"   Q_evap = {Q_evap:.2f} W")

    print("\n3. Balanço de energia:")
    print(f"   Q_cond = Q_evap + W_comp")
    print(f"   {Q_cond:.2f} = {Q_evap:.2f} + {W_comp:.2f}")
    print(f"   {Q_cond:.2f} ≈ {Q_evap + W_comp:.2f} W ✓")

    m = 0.0338362418
    w = 1667.3531
    QL_calc = Q_evap
    QH = Q_cond
    
    # PropriedadeS noS eStadoS
    # EStado 1: Saída do evaporador / Entrada do compreSSor (vapor Saturado)
    T1 = T_evap + 273
    P1 = CP.PropsSI('P', 'T', T1, 'Q', 1, liq_ref)
    H1 = CP.PropsSI('H', 'T', T1, 'Q', 1, liq_ref)
    S1 = CP.PropsSI('S', 'T', T1, 'Q', 1, liq_ref)
    
    # EStado 2: Saída do compreSSor / Entrada do condenSador (compreSSão iSentrópica)
    
    # EStado 3: Saída do condenSador / Entrada do capilar (líquido Saturado)
    T3 = T_cond + 273
    P3 = CP.PropsSI('P', 'T', T3, 'Q', 0, liq_ref)
    H3 = CP.PropsSI('H', 'T', T3, 'Q', 0, liq_ref)
    S3 = CP.PropsSI('S', 'T', T3, 'Q', 0, liq_ref)

    H2 = H1+w/m

    P2 = P3
    S2 = CP.PropsSI('S', 'P', P2, 'H', H2, liq_ref)
    T2 = CP.PropsSI('T', 'P', P2, 'H', H2, liq_ref)
    
    # EStado 4: Saída do capilar / Entrada do evaporador (expanSão iSentálpica)
    T4 = T1
    P4 = P1
    H4 = H3  # ExpanSão iSentálpica
    S4 = S3


    df_ciclo_real = pd.DataFrame({
        'Entrada': ['Compressor', 'Condensador', 'Capilar', 'Evaporador'],
        'T': [T1, T2, T3, T4],
        'P': [P1, P2, P3, P4],
        'H': [H1, H2, H3, H4],
        'S': [S1, S2, S3, S4],
        }, index=[1, 2, 3, 4] )

    real_dict={
        "compressor": "NJ9238E_15467BTU",
        "COP": COP,
        "QL": QL_calc,
        "QH": QH,
        "m": m,
        "w": w,
        "df_ciclo": df_ciclo_real
    }


    return real_dict

# calc_inverno("R22")