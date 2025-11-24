# Requerimentos

## Objetivos do trabalho:
1. Contextualizar a cidade, seu clima e a variação anual de temperaturas.
2. Especificar o compressor utilizado e suas curvas de vazão mássica e potência
ajustadas para simulação;
3. Obter os parâmetros UA dos trocadores, projetando para uma diferença de temperatura
de 5 °C nos trocadores na estação que mais demanda do sistema.
4. Simular o comportamento do sistema projetado ao ser acionado inversamente.

## Condições de Contorno:

> Na estação que mais demanda do sistema:
1. Temperatura interna: Ti = 18°C
2. Capacidade necessária: Qh ou Ql = 15000 BTU

# Afazeres

- [x] Ciclo Carnot, para ambos os cenários
- [x] Portabilidade curvas termo
- [x] Cálculo das temperaturas ambientes (temperaturas dos trocados com 5°C de diferença)
- [x] Selecionar compressores, HBP, assumindo 15000 BTU por hora, Liq_ref = R22
- [ ] Gráfico para plotar curvas compressores [massa e potência]
- [ ] Cálculo trocadores
  - [x] Descobrir UA para a situação
  - [ ] Calcular calor saindo dos trocadores (QH)
  - Temperaturas extremas ambiente: __35°C e 9°C__
- [ ] Selecionar 4 Curiosidades do Cairo
