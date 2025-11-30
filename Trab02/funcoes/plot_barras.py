import matplotlib.pyplot as plt
import pandas as pd
import os
from pathlib import Path
import matplotlib.cm as cm
import numpy as np

def plotar_comparacao_compressores(df, pasta_saida='graficos_compressores'):
    """
    Cria gráficos de barras comparativos para cada coluna do dataframe.
    
    Parameters:
    -----------
    df : pd.DataFrame
        DataFrame com dados dos compressores
    pasta_saida : str
        Caminho da pasta onde os gráficos serão salvos
    """
    
    # Criar pasta de saída se não existir
    Path(pasta_saida).mkdir(parents=True, exist_ok=True)
    
    # Gerar cores automaticamente usando um colormap

    
    # Número de compressores
    n_compressores = len(df['compressor'])
    
    # Gerar cores distintas automaticamente
    cmap = cm.get_cmap('tab10')  # Usar colormap com cores distintas
    cores = [cmap(i % 10) for i in range(n_compressores)]
    
    # Definir informações das colunas (título e unidade)
    info_colunas = {
        'COP': {
            'titulo': 'Coeficiente de Performance (COP)',
            'ylabel': 'COP [-]'
        },
        'QL': {
            'titulo': 'Capacidade de Refrigeração',
            'ylabel': 'QL [W]'
        },
        'QH': {
            'titulo': 'Capacidade de Aquecimento',
            'ylabel': 'QH [W]'
        },
        'm': {
            'titulo': 'Vazão Mássica',
            'ylabel': 'm [kg/s]'
        },
        'w': {
            'titulo': 'Trabalho do Compressor',
            'ylabel': 'W [W]'
        },
        'UA_externo': {
            'titulo': 'Coeficiente Global de Troca de Calor (UA)',
            'ylabel': 'UA [W/K]'
        },
        'UA_interno': {
            'titulo': 'Coeficiente Global de Troca de Calor (UA)',
            'ylabel': 'UA [W/K]'
        },
    }
    
    figsize = (10, 6)
    
    # Plotar gráfico para cada coluna (exceto 'compressor')
    for coluna in df.columns:
        if coluna == 'compressor':
            continue
        
        # Criar figura
        plt.figure(figsize=figsize)
        
        # Criar gráfico de barras
        bars = plt.bar(df['compressor'], df[coluna], color=cores, 
                       edgecolor='black', linewidth=1.2, alpha=0.8)
        
        # Configurar título e labels
        info = info_colunas.get(coluna, {
            'titulo': coluna,
            'ylabel': coluna
        })
        
        plt.title(info['titulo'], fontsize=14, fontweight='bold', pad=15)
        plt.ylabel(info['ylabel'], fontsize=11)
        plt.xlabel('Compressor', fontsize=11)
        
        
        match coluna:
            case "m":
                for bar in bars:
                    height = bar.get_height()
                    plt.text(bar.get_x() + bar.get_width()/2., height,
                            f'{height:.4f}',
                            ha='center', va='bottom', fontsize=9)
            case _:
                for bar in bars:
                    height = bar.get_height()
                    plt.text(bar.get_x() + bar.get_width()/2., height,
                            f'{height:.2f}',
                            ha='center', va='bottom', fontsize=9)
        
        # Rotacionar labels do eixo x se necessário
        plt.xticks(rotation=45, ha='right')
        
        # Ajustar grid
        plt.grid(axis='y', alpha=0.3, linestyle='--')
        
        # Ajustar layout
        plt.tight_layout()
        
        # Salvar figura
        nome_arquivo = f'{coluna}_comparacao.png'
        caminho_completo = os.path.join(pasta_saida, nome_arquivo)
        plt.savefig(caminho_completo, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f'Gráfico salvo: {caminho_completo}')
    
    print(f'\nTodos os gráficos foram salvos em: {pasta_saida}')



    