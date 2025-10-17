

#? ================================= Calc Massa e Calor Peixe
dens_peixe = 972 # kg/m³
volume = 0.7*200 / (10**3) # cm³ para m³ Considerando 70% do volume total
m = dens_peixe*volume

def calc_Q(massa, calor, diff_temp):
    Q = massa*calor*diff_temp
    return Q

Q_resfriando = calc_Q(m, 0.82 * 4.184, 30)
Q_muda_fase = calc_Q(m, 56 * 4.184, 1)
Q_congelado = calc_Q(m, 0.41 * 4.184, 25)

Q_total = Q_resfriando + Q_muda_fase + Q_congelado
