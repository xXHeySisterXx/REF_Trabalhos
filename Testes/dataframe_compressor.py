
import pandas as pd

def dataframe_compressor():
    df_compressor = pd.read_csv('Trab01\programa\dados_compressores\EMI40HNR.csv', header=0, sep=';')

    return df_compressor

df_teste = dataframe_compressor()

print(df_teste.head(10))