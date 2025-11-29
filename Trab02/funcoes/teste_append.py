import pandas as pd


lista_compressores=["NJ7240F_19462", "NJ9232E_12240", "NJ9232E_13949", "NJ9238E_15467"]
resultados=[]



for i, compressor in enumerate(lista_compressores):

    dict_ex={
        'compressor': compressor,
        'iqua': i*i,
        'iquinta': i**5,
    }


    dict_ex.pop('iquinta')
    resultados.append(dict_ex)

compilado_compressores = pd.DataFrame(resultados)
print(compilado_compressores.head(10))