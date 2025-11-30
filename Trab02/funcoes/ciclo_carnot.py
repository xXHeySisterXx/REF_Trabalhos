import CoolProp.CoolProp as CP
import pandas as pd
import numpy as np




def carnot_temps_verao(TH, TL, QL, liq_ref):

    COP = TL/(TH-TL)

    T1=T4=TL
    T2=T3=TH

    S2 = CP.PropsSI("S", "T", TH, "Q", 1, liq_ref)
    S3 = CP.PropsSI("S", "T", TH, "Q", 0, liq_ref)
    S1=S2
    S4=S3

    H1=CP.PropsSI("H", "T", TL, "S", S2, liq_ref)
    H2=CP.PropsSI("H", "T", TH, "Q", 1, liq_ref)
    H3=CP.PropsSI("H", "T", TH, "Q", 0, liq_ref)
    H4=CP.PropsSI("H", "T", TL, "S", S3, liq_ref)

    P1=CP.PropsSI("P", "T", TL, "S", S2, liq_ref)
    P2=CP.PropsSI("P", "T", TH, "Q", 1, liq_ref)
    P3=CP.PropsSI("P", "T", TH, "Q", 0, liq_ref)
    P4=CP.PropsSI("P", "T", TL, "S", S3, liq_ref)


    m = QL/(H1-H4)

    QH = m*(H2-H3)

    df_ciclo = pd.DataFrame({
        'Entrada': ['Compressor', 'Condensador', 'Capilar', 'Evaporador'],
        'T': [T1, T2, T3, T4],
        'P': [P1, P2, P3, P4],
        'H': [H1, H2, H3, H4],
        'S': [S1, S2, S3, S4],
        }, index=[1, 2, 3, 4] )

    carnot_dict={
        "compressor": "Ideal",
        "COP": COP,
        "QL": QL,
        "QH": QH,
        "m": m,
        "w": QL/COP,
        "df_ciclo": df_ciclo
    }

    return carnot_dict

def carnot_temps_inverno(TH, TL, QH, liq_ref):

    COP = TL/(TH-TL)
    QL= COP*QH/(COP+1)


    T1=T4=TL
    T2=T3=TH

    S2 = CP.PropsSI("S", "T", TH, "Q", 1, liq_ref)
    S3 = CP.PropsSI("S", "T", TH, "Q", 0, liq_ref)
    S1=S2
    S4=S3

    H1=CP.PropsSI("H", "T", TL, "S", S2, liq_ref)
    H2=CP.PropsSI("H", "T", TH, "Q", 1, liq_ref)
    H3=CP.PropsSI("H", "T", TH, "Q", 0, liq_ref)
    H4=CP.PropsSI("H", "T", TL, "S", S3, liq_ref)
    
    P1=CP.PropsSI("P", "T", TL, "S", S2, liq_ref)
    P2=CP.PropsSI("P", "T", TH, "Q", 1, liq_ref)
    P3=CP.PropsSI("P", "T", TH, "Q", 0, liq_ref)
    P4=CP.PropsSI("P", "T", TL, "S", S3, liq_ref)

    df_ciclo = pd.DataFrame({
        'Entrada': ['Compressor', 'Condensador', 'Capilar', 'Evaporador'],
        'T': [T1, T2, T3, T4],
        'P': [P1, P2, P3, P4],
        'H': [H1, H2, H3, H4],
        'S': [S1, S2, S3, S4],
        }, index=[1, 2, 3, 4] )

    QH = H2-H3
    m = QL/(H1-H4)

    carnot_dict={
        "compressor": "Ideal",
        "COP": COP,
        "QL": QL,
        "QH": QH,
        "m": m,
        "w": QH/COP,
        "df_ciclo": df_ciclo
    }

    return carnot_dict