from funcoes.ciclo_carnot import *
from funcoes.print_ciclo import *
from funcoes.calc_ciclo import*

#* Conversões:
BTU_to_W = 0.293
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
NJ9232E_12240
NJ9232E_13949
NJ9238E_15467
"""


#* Condições ideais:
carnot_verao = carnot_temps_verao(TH=T_ext_verao, TL=T_interior, QL=Capacidade_necessaria_W, liq_ref=liq_ref)
carnot_inverno = carnot_temps_inverno(TH=T_interior, TL=T_ext_inverno, QH=Capacidade_necessaria_W, liq_ref=liq_ref)

print("\nCondições Ideais Verão:\n", carnot_verao)
print("\nCondições Ideais Inverno:\n", carnot_inverno)

plot_ciclo(df_ciclo_ideal = carnot_verao["df_ciclo"],  liq_ref=liq_ref, descricao= "Ciclo para o extremo Verão")
plot_ciclo(df_ciclo_ideal = carnot_inverno["df_ciclo"],  liq_ref=liq_ref, descricao="Ciclo para o extremo Inverno")

#* Tratamento compressores:
# lista_compressores=["NJ7240F_19462", "NJ9232E_12240", "NJ9232E_13949", "NJ9238E_15467"]
# for compressor in lista_compressores:
compressor = "NJ7240F_19462"
funcao_padrao_real(Capacidade_necessaria_W, compressor, liq_ref)
