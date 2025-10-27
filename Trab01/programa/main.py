import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.optimize import brentq

from calc_auxiliar import*
from calc_COP import*
from calc_ciclo_padrao import*
from ciclo_padrao_real import*
from calc_otimização import*
from plot_barras import*


# Mostrar todas as colunas
pd.set_option('display.max_columns', None)

# Mostrar todas as linhas
pd.set_option('display.max_rows', None)

# Largura máxima para cada coluna
pd.set_option('display.max_colwidth', None)

# Largura total do display
pd.set_option('display.width', 0)  # Deixa o pandas calcular automaticamente

# Evita o uso de quebra de linha para colunas grandes
pd.set_option('display.expand_frame_repr', False)



# class componente:
#     def __init__(self, temp, pres, ):
#         self.temp = temp

# ?=================== Massa e Calor
dens_peixe = 972 # kg/m³
volume = 0.7*200 / (10**3) # cm³ para m³ Considerando 70% do volume total
m = dens_peixe*volume


Q_congelado = (calc_Q(m, 0.41 * 4.184, 25))*1000

QL = Q_congelado / (8*60*60) # W

# QL = 202.6 para levar de 0 a -25

# ?=================== Ciclos


compressor_lista = ["EGZS70HLC_202W", "FFU70HAK_221W"]
liq_refrigerante = "R134a"

valores_barras=[]


for compressor in compressor_lista:

    df_ciclo_padrao = ciclo_padrao(T_amb = 35 + 273, T_int = -25 + 273, QL=QL, liq_refrigerante=liq_refrigerante)

    serie_ciclo_real = funcao_padrao_real(QL, -25 + 273, compressor)
    df_ciclo_real = pontos_ciclo(serie_ciclo_real, liq_refrigerante)

    serie_otima = otimizar_ciclo(QL_desejado=QL, compressor= compressor)
    df_ciclo_otimo = pontos_ciclo_otimo(serie_otima, liq_refrigerante)


    plot_ciclo(df_ciclo_padrao, df_ciclo_real, df_ciclo_otimo, liq_refrigerante, compressor)

    resultado ={
        'W_ideal': df_ciclo_padrao.loc[1,'W'],
        'QL_ideal': QL,
        'm_ideal': df_ciclo_padrao.loc[1,'m'],
        'COP_ideal': df_ciclo_padrao.loc[1,'COP'],
        'W_real': df_ciclo_real.loc[1,'W'],
        'QL_real': df_ciclo_real.loc[1,'QL'],
        'm_real': df_ciclo_real.loc[1,'m'],
        'COP_real' : df_ciclo_real.loc[1,'COP'],
        'W_otimo': df_ciclo_otimo.loc[1,'W'],
        'QL_otimo': df_ciclo_otimo.loc[1,'QL'],
        'm_otimo': df_ciclo_otimo.loc[1,'m'],
        'COP_otimo': df_ciclo_otimo.loc[1,'COP'],
    }

    valores_barras.append(resultado)

df_plot_barras = pd.DataFrame(valores_barras, index=compressor_lista)

plot_barras(df_plot_barras, liq_refrigerante, compressor)



#! EMIE40HER tem T3>T2, estranho