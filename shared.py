import pandas as pd

df_tratado = pd.read_csv("dataset_final.csv", sep=";", low_memory=False, index_col=0)
