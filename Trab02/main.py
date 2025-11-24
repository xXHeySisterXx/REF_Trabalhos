from funcoes.ciclo_carnot import *
from funcoes.print_ciclo import *

from funcoes.calc_UA import*

#* Conversões:
BTU_to_W = 0.293 # ( BTU por Hora )
C_to_K = 273


#* Condições de contorno:
liq_ref = "R22"
Capacidade_necessaria = 15000 * BTU_to_W
T_ext_verao = 35 + C_to_K # Temperatura externa no verao
T_ext_inverno = 9 + C_to_K # Temperatura externa no inverno
T_interior = 18 + C_to_K


#* Condições ideais:
carnot_verao = carnot_temps_verao(TH=T_ext_verao, TL=T_interior, QL=Capacidade_necessaria, liq_ref=liq_ref)
carnot_inverno = carnot_temps_inverno(TH=T_interior, TL=T_ext_inverno, QH=Capacidade_necessaria, liq_ref=liq_ref)

print("\nCondições Ideais Verão:\n", carnot_verao)
print("\nCondições Ideais Inverno:\n", carnot_inverno)

plot_ciclo(df_ciclo_ideal = carnot_verao["df_ciclo"],  liq_ref=liq_ref, descricao= "Ciclo para o extremo Verão")
plot_ciclo(df_ciclo_ideal = carnot_inverno["df_ciclo"],  liq_ref=liq_ref, descricao="Ciclo para o extremo Inverno")


#! Q que vai para o exterior, depende o ciclo
UA_verao = calc_UA(Q=Q_ext_verao,
        diff_temp=5)

UA_inverno = calc_UA(Q=Q_ext_inverno,
        diff_temp=5)