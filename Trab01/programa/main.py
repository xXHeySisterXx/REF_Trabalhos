import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.optimize import brentq

from calc_auxiliar import*
from calc_COP import*
from calc_ciclo_padrao import*
from ciclo_padrao_real import*


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


Q_congelado = (calc_Q(m, 0.41 * 4.184, 23))*1000 # Todo verificar temperatura de transporte peixe

QL = Q_congelado / (8*60*60) # W



# ?=================== Ciclo padrão
# df_ciclo_padrao = ciclo_padrao(T_amb = 35 + 273, T_int = -25 + 273, QL=QL, liq_refrigerante='R134a')
# plot_ciclo(df_ciclo_padrao, 'R134a')

serie_ciclo_real = funcao_padrao_real(QL, -25 + 273, "EMI40HNR")
df_ciclo_real = pontos_ciclo(serie_ciclo_real, "R134a")
plot_ciclo(df_ciclo_real, 'R134a')

#! EMIE40HER tem T3>T2, estranho