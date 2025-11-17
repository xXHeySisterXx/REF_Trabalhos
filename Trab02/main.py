from funcoes.ciclo_carnot import *

#* Conversões:
BTU_to_W = 0.293
C_to_K = 273

#* Condições de contorno:
liq_ref = "R134a"
Capacidade_necessaria = 15000 * BTU_to_W
T_ext_calor = 35 + C_to_K # Temperatura externa
T_interior = 18 + C_to_K

#* Condições ideais:
carnot_temps_dict = carnot_temps(Th=T_ext_calor, Tl=T_interior, Ql=Capacidade_necessaria, liq_ref=liq_ref)

print("\nCondições Ideais:\n", carnot_temps_dict)