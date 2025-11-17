import pandas as pd
import numpy as np
import CoolProp.CoolProp as CP
import matplotlib.pyplot as plt

from domo import domo_refrigerante



def plot_ciclo (df_ciclo_ideal=None, df_ciclo_real=None, df_ciclo_otimo=None,  liq_ref="R134a", compressor='1'):
    df_domo = domo_refrigerante(liq_ref)

    
    fig, (TS, PH) = plt.subplots(1, 2, figsize = (12, 4))

    TS.plot(df_domo['S'], df_domo['T'],)
    PH.plot(df_domo['H'], df_domo['P'],)

    if df_ciclo_ideal is not None and not df_ciclo_ideal.empty:
        TS.plot(df_ciclo_ideal['S']/1000, df_ciclo_ideal['T'], label = "Ideal", marker = "x")
        PH.plot(df_ciclo_ideal['H']/1000, df_ciclo_ideal['P']/1000, label = "Ideal", marker = "x")


    if df_ciclo_real is not None and not df_ciclo_real.empty:
        TS.plot(df_ciclo_real['S']/1000, df_ciclo_real['T'], label = "Real", marker = ".")
        PH.plot(df_ciclo_real['H']/1000, df_ciclo_real['P']/1000, label = "Real", marker = ".")

    if df_ciclo_otimo is not None and not df_ciclo_otimo.empty:
        TS.plot(df_ciclo_otimo['S']/1000, df_ciclo_otimo['T'], label = "Ótimo", marker = "^")
        PH.plot(df_ciclo_otimo['H']/1000, df_ciclo_otimo['P']/1000, label = "Ótimo", marker = "^")

    # for idx, row in df_ciclo_ideal.iloc[:-1].iterrows():
    #     PH.text(
    #         row['H']/1000, 
    #         row['P']/1000, 
    #         row['Entrada'],
    #         fontsize=9,
    #         ha='right',  # alinhamento horizontal: 'left', 'right', 'center'
    #         va='bottom'  # alinhamento vertical: 'top', 'bottom', 'center'
    #     )
    #     TS.text(
    #         row['S']/1000, 
    #         row['T'], 
    #         row['Entrada'],
    #         fontsize=9,
    #         ha='right',  # alinhamento horizontal: 'left', 'right', 'center'
    #         va='bottom'  # alinhamento vertical: 'top', 'bottom', 'center'
    #     )

    # for idx, row in df_ciclo_real.iloc[:-1].iterrows():
    #     PH.text(
    #         row['H']/1000, 
    #         row['P']/1000, 
    #         row['Entrada'],
    #         fontsize=9,
    #         ha='right',  # alinhamento horizontal: 'left', 'right', 'center'
    #         va='bottom'  # alinhamento vertical: 'top', 'bottom', 'center'
    #     )
    #     TS.text(
    #         row['S']/1000, 
    #         row['T'], 
    #         row['Entrada'],
    #         fontsize=9,
    #         ha='right',  # alinhamento horizontal: 'left', 'right', 'center'
    #         va='bottom'  # alinhamento vertical: 'top', 'bottom', 'center'
    #     )


    TS.set_xlabel("Entropia [kJ/kgK]")
    TS.set_ylabel("Temperatura [K]")

    PH.set_xlabel("Entalpia [kJ/kg]")
    PH.set_ylabel("Pressão [kPa]")

    PH.minorticks_on()
    PH.grid(True, which='major', linestyle = '-', linewidth = 1.0)
    PH.grid(True, which='minor', linestyle = ':', linewidth = 0.5, alpha = 0.7)

    TS.minorticks_on()
    TS.grid(True, which='major', linestyle = '-', linewidth = 1.0)
    TS.grid(True, which='minor', linestyle = ':', linewidth = 0.5, alpha = 0.7)

    PH.legend()
    TS.legend()

    fig.suptitle(f'Ciclo para {compressor}', fontsize=16)
    plt.tight_layout()
    # plt.show()
    PH.figure.savefig(
        f'Trab01\\programa\\Graficos\\ciclo_{compressor}',
        dpi=300,
        bbox_inches='tight',
        transparent=True,
        facecolor='white',
)
    return

