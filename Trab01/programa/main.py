import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.optimize import brentq

from calc_auxiliar import*
from calc_COP import*
from calc_ciclo_padrao import*



# class componente:
#     def __init__(self, temp, pres, ):
#         self.temp = temp

# ?=================== Massa e Calor
dens_peixe = 972 # kg/m³
volume = 0.7*200 / (10**3) # cm³ para m³ Considerando 70% do volume total
m = dens_peixe*volume


Q_congelado = (calc_Q(m, 0.41 * 4.184, 10))*1000 # Todo verificar temperatura de transporte peixe

QL = Q_congelado / (8*60*60) # W



# ?=================== Ciclo padrão
df_ciclo_padrao = ciclo_padrao(T_amb = 35 + 273, T_int = -25 + 273, QL=QL, liq_refrigerante='R134a')
plot_ciclo(df_ciclo_padrao, 'R134a')