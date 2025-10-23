import os
import pandas as pd
from pathlib import Path

def processar_csvs(pasta):
    """
    Lê todos os arquivos CSV de uma pasta, soma 273 às colunas
    T_condensador e T_evaporador, e salva sobre os arquivos originais.
    
    Args:
        pasta: Caminho da pasta contendo os arquivos CSV
    """
    # Converter para Path para facilitar manipulação
    pasta_path = Path(pasta)
    
    # Verificar se a pasta existe
    if not pasta_path.exists():
        print(f"Erro: A pasta '{pasta}' não existe!")
        return
    
    # Buscar todos os arquivos .csv na pasta
    arquivos_csv = list(pasta_path.glob("*.csv"))
    
    if not arquivos_csv:
        print(f"Nenhum arquivo CSV encontrado na pasta '{pasta}'")
        return
    
    print(f"Encontrados {len(arquivos_csv)} arquivo(s) CSV\n")
    
    # Processar cada arquivo
    for arquivo in arquivos_csv:
        try:
            print(f"Processando: {arquivo.name}")
            
            # Ler o CSV
            df = pd.read_csv(arquivo, sep=';')
            
            # Verificar se as colunas existem
            colunas_modificadas = []
            
            if 'T_condensador' in df.columns:
                df['T_condensador'] = df['T_condensador'] + 273
                colunas_modificadas.append('T_condensador')
            
            if 'T_evaporador' in df.columns:
                df['T_evaporador'] = df['T_evaporador'] + 273
                colunas_modificadas.append('T_evaporador')
            
            if colunas_modificadas:
                # Salvar sobre o arquivo original
                df.to_csv(arquivo, index=False)
                print(f"  ✓ Modificadas: {', '.join(colunas_modificadas)}")
            else:
                print(f"  ⚠ Colunas T_condensador e T_evaporador não encontradas")
            
        except Exception as e:
            print(f"  ✗ Erro ao processar {arquivo.name}: {str(e)}")
        
        print()
    
    print("Processamento concluído!")


if __name__ == "__main__":
    # Definir o caminho da pasta diretamente
    pasta_csvs = "Testes/dados_compressores"
    
    print(f"Iniciando processamento...")
    print(f"Pasta especificada: {pasta_csvs}")
    print(f"Diretório atual: {os.getcwd()}\n")
    
    processar_csvs(pasta_csvs)