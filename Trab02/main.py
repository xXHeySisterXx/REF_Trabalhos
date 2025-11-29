from funcoes.ciclo_carnot import *
from funcoes.print_ciclo import *
from funcoes.calc_ciclo import*
from funcoes.plot_barras import*
import pandas as pd

from funcoes.calc_UA import*

#* Conversões:
BTU_to_W = 0.293 # ( BTU por Hora )
C_to_K = 273


#* Condições de contorno:
liq_ref = "R22"
Capacidade_necessaria_W = 15000 * BTU_to_W
T_ext_verao = 35 + C_to_K # Temperatura externa no verao
T_ext_inverno = 9 + C_to_K # Temperatura externa no inverno
T_interior = 18 + C_to_K

"""
Lista compressores:
NJ7240F_19462
NJ9238E_15467
NJ9232E_13949
NJ9232E_12240
"""
# lista_compressores=["NJ7240F_19462BTU", "NJ9232E_12240BTU", "NJ9232E_13949BTU", "NJ9238E_15467BTU"]

resultados_verao=[]
resultados_inverno=[]

#* Condições ideais:

carnot_verao = carnot_temps_verao(TH=T_ext_verao, TL=T_interior, QL=Capacidade_necessaria_W, liq_ref=liq_ref)
print("\nCondições Ideais Verão:\n", carnot_verao)
# plot_ciclo(df_ciclo_ideal = carnot_verao["df_ciclo"],  liq_ref=liq_ref, descricao= "Ciclo para o extremo Verão")

# carnot_inverno = carnot_temps_inverno(TH=T_interior, TL=T_ext_inverno, QH=Capacidade_necessaria_W, liq_ref=liq_ref) #todo verificar modificações dict, QH e m
# print("\nCondições Ideais Inverno:\n", carnot_inverno)
# plot_ciclo(df_ciclo_ideal = carnot_inverno["df_ciclo"],  liq_ref=liq_ref, descricao="Ciclo para o extremo Inverno")


carnot_verao.pop('df_ciclo')
resultados_verao.append(carnot_verao)

# #* Cálculo ciclos:
# # for compressor in lista_compressores:
compressor = "NJ7240F_19462BTU"

real_dict_verao = funcao_padrao_real(Capacidade_necessaria_W, compressor, liq_ref, T_ext_verao+5, T_interior-5)
print("\nCondições Reais Verão:\n", real_dict_verao)
plot_ciclo(df_ciclo_real = real_dict_verao['df_ciclo'],  liq_ref=liq_ref, descricao="Ciclo real para o extremo Verão")


# real_dict_inverno = funcao_padrao_real(Capacidade_necessaria_W, compressor, liq_ref, T_interior+5, T_ext_inverno-5)
# print("\nCondições Ideais Verão:\n", real_dict_inverno)
# plot_ciclo(df_ciclo_ideal = real_dict_inverno["df_ciclo"],  liq_ref=liq_ref, descricao="Ciclo real para o extremo Inverno")


#* Cálculo UA:
# real_dict_verao['UA_externo_verao'] = calc_UA(Q=real_dict_verao['QH'], diff_temp=5) # W/K
# real_dict_verao['UA_interno_verao'] = calc_UA(Q=real_dict_verao['QL'], diff_temp=5)

# UA_externo_inverno = calc_UA(Q=real_dict_inverno['QH'], diff_temp=5)
# UA_interno_inverno = calc_UA(Q=real_dict_inverno['QL'], diff_temp=5)

real_dict_verao.pop('df_ciclo')
resultados_verao.append(real_dict_verao)

# real_dict_inverno.pop('df_ciclo')
# resultados_inverno.append(real_dict_verao)
# return

#* União dataframes

compilado_compressores = pd.DataFrame(resultados_verao)
print(compilado_compressores.head(10))

#* Plot barras:
plotar_comparacao_compressores(compilado_compressores, pasta_saida='Trab02/graficos_compressores')