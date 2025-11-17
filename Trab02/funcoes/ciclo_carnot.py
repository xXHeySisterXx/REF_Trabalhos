import CoolProp.CoolProp as CP
import pandas as pd
import numpy as np




def carnot_temps(Th, Tl, Ql, liq_ref):
    COP = Tl/(Th-Tl)

    S2 = CP.PropsSI("S", "T", Th, "Q", 1, liq_ref)
    S3 = CP.PropsSI("S", "T", Th, "Q", 0, liq_ref)

    carnot_temps_dict={
        "COP": COP,
        "w": Ql/COP,
        "H1": CP.PropsSI("H", "T", Tl, "S", S2, liq_ref),
        "H2": CP.PropsSI("H", "T", Th, "Q", 1, liq_ref),
        "H3": CP.PropsSI("H", "T", Th, "Q", 0, liq_ref),
        "H4": CP.PropsSI("H", "T", Tl, "S", S3, liq_ref),
        "P1": CP.PropsSI("P", "T", Tl, "S", S2, liq_ref),
        "P2": CP.PropsSI("P", "T", Th, "Q", 1, liq_ref),
        "P3": CP.PropsSI("P", "T", Th, "Q", 0, liq_ref),
        "P4": CP.PropsSI("P", "T", Tl, "S", S3, liq_ref),
    }

    return carnot_temps_dict