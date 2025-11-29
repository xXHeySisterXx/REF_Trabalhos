import pandas as pd
import numpy as np
import CoolProp.CoolProp as CP
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit



#? ================================= Quantidade de calor
def calc_Q(massa, calor, diff_temp=1):
    Q = massa*calor*diff_temp
    return Q


#? ================================= Domo fases liq
def domo_refrigerante(liq_refrigerante):

    T_min = CP.PropsSI('Tmin', liq_refrigerante)
    T_max = CP.PropsSI('Tcrit', liq_refrigerante)

    valores_T = np.linspace(T_min, T_max, 2000) # Liquido Saturado
    valores_H = []
    valores_P = []
    valores_S = []


    for T in valores_T:
        valores_H.append(CP.PropsSI('H', 'T', T, 'Q', 0, liq_refrigerante))
        valores_P.append(CP.PropsSI('P', 'T', T, 'Q', 0, liq_refrigerante))
        valores_S.append(CP.PropsSI('S', 'T', T, 'Q', 0, liq_refrigerante))

    valores_T_invertida = np.flip(valores_T)

    for T in valores_T_invertida:
            valores_H.append(CP.PropsSI('H', 'T', T, 'Q', 1, liq_refrigerante))
            valores_P.append(CP.PropsSI('P', 'T', T, 'Q', 1, liq_refrigerante))
            valores_S.append(CP.PropsSI('S', 'T', T, 'Q', 1, liq_refrigerante))

    valores_T_total = np.concatenate([valores_T, valores_T_invertida])
            
    df_domo = pd.DataFrame({
        'H': np.array(valores_H) / 1000,
        'P': np.array(valores_P) / 1000,
        'T': np.array(valores_T_total),
        'S': np.array(valores_S) / 1000,
    })

    return df_domo

def plot_ciclo (df_ciclo_ideal, df_ciclo_real, df_ciclo_otimo,  liq_refrigerante, compressor):
    df_domo = domo_refrigerante(liq_refrigerante)

    
    fig, (TS, PH) = plt.subplots(1, 2, figsize = (12, 4))

    TS.plot(df_domo['S'], df_domo['T'],)
    PH.plot(df_domo['H'], df_domo['P'],)

    TS.plot(df_ciclo_ideal['S']/1000, df_ciclo_ideal['T'], label = "Ideal", marker = "x")
    PH.plot(df_ciclo_ideal['H']/1000, df_ciclo_ideal['P']/1000, label = "Ideal", marker = "x")

    TS.plot(df_ciclo_real['S']/1000, df_ciclo_real['T'], label = "Real", marker = ".")
    PH.plot(df_ciclo_real['H']/1000, df_ciclo_real['P']/1000, label = "Real", marker = ".")

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


def dataframe_compressor(compressor):
    df_compressor = pd.read_csv(f'Trab01\programa\dados_compressores\{compressor}.csv', header=0, sep=';')

    return df_compressor

def ajuste_curva_massa(T1, P1, P2, df_compressor):

    N = 60 # Hz

    def funcao_massa(T1, b0, b1, b2):
        m = (P1*N)/T1 * (b0 - b1 * (( (P2/P1)**b2) - 1 ))
        return m
    
    params_massa, _ = curve_fit(funcao_massa, df_compressor['T_evaporador'], df_compressor['fluxo_massa']/(60*60))
    b0, b1, b2 = params_massa
    m = funcao_massa(T1, b0, b1, b2)

    # fig, (ax) = plt.subplots(figsize = (4,8))

    # ax.plot(df_compressor['T_evaporador'], df_compressor['fluxo_massa'], color = 'r', marker = '.')
    # ax.plot(df_compressor['T_evaporador'], funcao_massa(df_compressor['T_evaporador'], *params_massa), '-b')

    # plt.legend()
    # plt.tight_layout()
    # plt.show()

    return m



def ajuste_curva_potencia(m, T1, P1, P2, df_compressor):
    """
    T1 = Ts (sucção)

    """

    def funcao_potencia(T1, a0, a1, a2):
        w = m* ( a0*T1* ((P2/P1)**a1 - 1) + a2)
        return w

    params_potencia, _ = curve_fit(funcao_potencia, df_compressor['T_evaporador'], df_compressor['capacidade'])
    a0, a1, a2 = params_potencia
    w = funcao_potencia(T1, a0, a1, a2)

    H1 = CP.PropsSI('H', 'T', T1, 'Q', 1, "R134a") # [J/kgK]
    H2 = H1 + w/m + a2*10**-3

    # fig, (ax) = plt.subplots(figsize = (4,8))

    # ax.plot(df_compressor['T_evaporador'], df_compressor['capacidade'], color = 'r', marker = '.')
    # ax.plot(df_compressor['T_evaporador'], funcao_potencia(df_compressor['T_evaporador'], *params_potencia), '-b')

    # plt.legend()
    # plt.tight_layout()
    # plt.show()


    return w, H2
