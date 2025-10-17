# Anotações Simulação Refrigerador:
**Data entrega: 30/10**

## Observações:

O tempo de pulldown é que determina T_evaporador e T_condensador

Q_L é o requerimento do projeto, Q_total sobre o tempo


## Requerimentos:

1. O sistema deve funcionar em um ambiente a 35 °C
2. O sistema irá refrigerar um compartimento de 200L, e deverá atingir a temperatura
de operação desejada em no máximo 8 horas (tempo de pulldown)
3. A sua maior preocupação no projeto é o custo inicial

### Deve Possuir:

- [x] A contextualização e temperatura do item a ser refrigerado;
>   Temperatura (Longo prazo) = -25°C\
>   Alimento: Peixe \
>   Calor específico resfriado [HeatCraft]: 0,82 kcal/(kg C)
>   Calor específico congelado [HeatCraft]: 0,41 kcal/(kg C)
>   Calor Latente: 58.25 kcal/(kg C)
>   Densidade: 972 kg/m^3
>   Massa armazenada [200L]: 136 kg (70% do volume)

- [x] A escolha justificada do fluido refrigerante;
>R-404A: É um HFC (hidrofluorcarboneto) que por muito tempo foi padrão em sistemas de refrigeração de baixa e média temperatura, especialmente em balcões comerciais e câmaras frias. No entanto, devido ao seu alto potencial de aquecimento global (GWP), está sendo gradualmente substituído.
>R134a para forçar T2=T3 e P2=P3, que o Coolprop não consegue com fluidos misturados.


- [ ] A configuração do ciclo padrão de refrigeração (temperaturas, pressões e COP);

- [ ] A escolha de um compressor comercialmente disponível que funcione no ciclo apresentado e que fornece no mínimo a carga térmica descrita acima, citando a fonte do datasheet utilizado e como será feito o controle de capacidade;

- [ ] Os valores de potência de compressão e COP (usando dados experimentais do compressor e um modelo do ciclo de refrigeração padrão);

- [ ] Adicionar um condensador e um evaporador operando com 5 °C de diferença para o ambiente;

- [ ] Calcular a geração de entropia e a potência perdida associadas a cada componente;

- [ ] Comparar COP de Carnot, Ciclo Padrão, Ciclo com compressor real e ciclo com trocadores reais

## Afazeres:

### Preparatório:
- [ ] Elaborar diagrama com cálculos
- [x] Estimar carga de refrigeração
> Q_total = 51726.24 KJ
- [ ] Pacote para encontrar variáveis de curvas (ajusta curvas)

### Programa:
- [ ] Criação componentes
- [ ] inserir fórmulas

### Relatório:
- [ ] Criar arquivo relatório
- [ ] 
## 
