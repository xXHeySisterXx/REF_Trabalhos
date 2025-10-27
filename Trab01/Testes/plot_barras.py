import pandas as pd
import matplotlib.pyplot as plt

df = pd.DataFrame({
    'Série A': [10, 15, 12, 18],
    'Série B': [12, 18, 14, 20],
    'Série C': [0.00003, 13, 10, 16]
}, index=['Grupo 1', 'Grupo 2', 'Grupo 3', 'Grupo 4'])

ax = df.plot(kind='bar', figsize=(10, 6))

# Adicionar valores com formatação
for container in ax.containers:
    ax.bar_label(container, fmt='%.0f', fontsize=9, padding=2)

plt.ylabel('Valores')
plt.title('Gráfico de Barras Agrupadas')
plt.xticks(rotation=0)
plt.legend()
plt.tight_layout()
plt.show()