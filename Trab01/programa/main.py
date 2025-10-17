import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from calc_auxiliar import*
from calc_COP import*
from calc_ciclo_padrao import*

# class componente:
#     def __init__(self, temp, pres, ):
#         self.temp = temp

# =================== Massa e Calor
dens_peixe = 972 # kg/m³
volume = 0.7*200 / (10**3) # cm³ para m³ Considerando 70% do volume total
m = dens_peixe*volume

Q_resfriando = calc_Q(m, 0.82 * 4.184, 30)
Q_muda_fase = calc_Q(m, 56 * 4.184)
Q_congelado = calc_Q(m, 0.41 * 4.184, 25)

Q_total = Q_resfriando + Q_muda_fase + Q_congelado
QL = Q_total/ (8*60*60)

ciclo_padrao(T_amb = 35 + 273, T_int = -25 + 273, QL)

