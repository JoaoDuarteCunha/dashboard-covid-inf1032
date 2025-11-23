import pandas as pd

df_tratado = pd.read_csv("dataset_final.csv", sep=";", low_memory=False, index_col=0)
df_tratado["dataNotificacao"] = pd.to_datetime(
    df_tratado["dataNotificacao"].astype(str),
    errors="coerce",
)
df_tratado["classificacaoFinalSimplificado"] = None

# máscara dos negativos
mask_negativo = df_tratado["classificacaoFinal"].str.contains(
    "Não Especificada", case=False, na=False
) | df_tratado["classificacaoFinal"].str.contains("Descartado", case=False, na=False)

# atribui 0 para negativos
df_tratado.loc[mask_negativo, "classificacaoFinalSimplificado"] = 0

# atribui 1 para todos os demais (desde que não seja NaN)
df_tratado.loc[
    ~mask_negativo & df_tratado["classificacaoFinal"].notna(),
    "classificacaoFinalSimplificado",
] = 1
