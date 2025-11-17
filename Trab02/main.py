from funcoes.ciclo_carnot import *

#* Conversões:
BTU_to_W = 0.293
C_to_K = 273

#* Condições de contorno:
liq_ref = "R134a"
Capacidade_necessaria = 15000 * BTU_to_W
T_ext_verao = 35 + C_to_K # Temperatura externa no verao
T_ext_inverno = 9 + C_to_K # Temperatura externa no inverno
T_interior = 18 + C_to_K

#* Condições ideais:
carnot_verao = carnot_temps_verao(Th=T_ext_verao, Tl=T_interior, QL=Capacidade_necessaria, liq_ref=liq_ref)
carnot_inverno = carnot_temps_inverno(Th=T_interior, Tl=T_ext_inverno, QH=Capacidade_necessaria, liq_ref=liq_ref)

print("\nCondições Ideais Verão:\n", carnot_verao)
print("\nCondições Ideais Inverno:\n", carnot_inverno)