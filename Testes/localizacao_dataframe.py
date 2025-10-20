import pandas as pd

df_compressores = pd.DataFrame({
    'p0': [1],
    'p1': [1],
    'p2': [1],
    'p3': [1]
    })

p0 = df_compressores.loc[f"{compressor}", "p0"]
print(p0)
