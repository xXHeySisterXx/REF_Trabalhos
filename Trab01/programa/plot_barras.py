import pandas as pd
import matplotlib.pyplot as plt


def plot_barras(df_plot_barras, liq_refrigerante, compressor):
    
    # DataFrame W
    df_W = df_plot_barras[['W_ideal', 'W_real', 'W_otimo']]
    df_W.columns = ['Ideal', 'Real', 'Ótimo']
    
    # Plotar W
    fig1, ax1 = plt.subplots(figsize=(10, 6))
    df_W.plot(kind='bar', ax=ax1)
    ax1.bar_label(ax1.containers[0], fmt='%.1f', fontsize=9)
    ax1.bar_label(ax1.containers[1], fmt='%.1f', fontsize=9)
    ax1.bar_label(ax1.containers[2], fmt='%.1f', fontsize=9)
    ax1.set_ylabel('W [W]')
    ax1.set_title('Comparação de Potência')
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    fig1.savefig('Trab01/programa/Graficos/barras_W.png', dpi=300, bbox_inches='tight')
    
    # DataFrame COP
    df_COP = df_plot_barras[['COP_ideal', 'COP_real', 'COP_otimo']]
    df_COP.columns = ['Ideal', 'Real', 'Ótimo']
    
    # Plotar COP
    fig2, ax2 = plt.subplots(figsize=(10, 6))
    df_COP.plot(kind='bar', ax=ax2)
    ax2.bar_label(ax2.containers[0], fmt='%.1f', fontsize=9)
    ax2.bar_label(ax2.containers[1], fmt='%.1f', fontsize=9)
    ax2.bar_label(ax2.containers[2], fmt='%.1f', fontsize=9)
    ax2.set_ylabel('COP')
    ax2.set_title('Comparação de COP')
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    fig2.savefig('Trab01/programa/Graficos/barras_COP.png', dpi=300, bbox_inches='tight')
    
    # DataFrame m
    df_m = df_plot_barras[['m_ideal', 'm_real', 'm_otimo']]
    df_m.columns = ['Ideal', 'Real', 'Ótimo']
    
    # Plotar m
    fig3, ax3 = plt.subplots(figsize=(10, 6))
    df_m.plot(kind='bar', ax=ax3)
    ax3.bar_label(ax3.containers[0], fmt='%.2e', fontsize=8)
    ax3.bar_label(ax3.containers[1], fmt='%.2e', fontsize=8)
    ax3.bar_label(ax3.containers[2], fmt='%.2e', fontsize=8)
    ax3.set_ylabel('m [kg/s]')
    ax3.set_title('Comparação de Vazão Mássica')
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    fig3.savefig('Trab01/programa/Graficos/barras_m.png', dpi=300, bbox_inches='tight')
    
    # DataFrame QL
    df_QL = df_plot_barras[['QL_ideal', 'QL_real', 'QL_otimo']]
    df_QL.columns = ['Ideal', 'Real', 'Ótimo']
    
    # Plotar QL
    fig4, ax4 = plt.subplots(figsize=(10, 6))
    df_QL.plot(kind='bar', ax=ax4)
    ax4.bar_label(ax4.containers[0], fmt='%.1f', fontsize=9)
    ax4.bar_label(ax4.containers[1], fmt='%.1f', fontsize=9)
    ax4.bar_label(ax4.containers[2], fmt='%.1f', fontsize=9)
    ax4.set_ylabel('QL [W]')
    ax4.set_title('Comparação de Capacidade')
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    fig4.savefig('Trab01/programa/Graficos/barras_QL.png', dpi=300, bbox_inches='tight')
    
