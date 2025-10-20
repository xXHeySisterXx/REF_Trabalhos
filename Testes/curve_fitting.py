from scipy.optimize import curve_fit
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


x=np.linspace(0, 10, 50)
y_alvo = 2 * x**2 + 3 * x + 1 + np.random.normal(0, 5, 50)

def funcao_compressor(x, a0, a1, a2):
    return a0*x + a0*x**2 + a1*x**3 + a2*x**4


parametros_otimos, covariancia = curve_fit(funcao_compressor, x, y_alvo)

#? x(T_evaporador) e y_alvo(massa ou potência) serão colunas dataframe com a separação do np.where para a T_condensador


a_opt, b_opt, c_opt = parametros_otimos
print(f"Parâmetros ajustados: a={a_opt:.2f}, b={b_opt:.2f}, c={c_opt:.2f}")

# 4. Visualize o resultado
plt.scatter(x, y_alvo, label='Dados originais')
plt.plot(x, funcao_compressor(x, *parametros_otimos), 
         'r-', label='Função ajustada')
plt.legend()
plt.show()