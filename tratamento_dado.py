import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.preprocessing import MinMaxScaler, RobustScaler
from dicts import mapeamento_regiao, municipios_estados


def separaSintomas(celula):
    celula = celula.split(",")
    new_celula = []
    for sintoma in celula:
        sintoma = sintoma.strip()
        sintoma = sintoma.lower()
        new_celula.append(sintoma)
    return new_celula


def tratamento(df: pd.DataFrame):
    # Levantar todos os sintomas existentes
    sintomas_list = []
    df["sintomas"] = df["sintomas"].fillna("Ausência de sintomas primários")
    for celula in df["sintomas"]:
        if type(celula) == str:
            celula_list = separaSintomas(celula)
            for sintoma in celula_list:
                if sintoma not in sintomas_list:
                    sintomas_list.append(sintoma)
    sintomas_list.remove("")
    print(sintomas_list)

    for sintoma in sintomas_list:
        possui_sintoma = []
        i = 0
        for celula in df["sintomas"]:
            celula_list = separaSintomas(celula)
            if sintoma in celula_list:
                possui_sintoma.append(1)
            else:
                possui_sintoma.append(0)
            i += 1
        df[sintoma] = possui_sintoma
    df = df.drop(
        columns=["assintomático", "ausência de sintomas primários"], axis=1
    )  # Tirando colunas redundantes

    # Separando sintomas secundários
    sintomas_secundarios = []
    df["outrosSintomas"].fillna("Sem sintomas secundários")
    for celula in df["outrosSintomas"]:
        if type(celula) == str:
            celula = separaSintomas(celula)
            for sintoma in celula:
                if sintoma not in sintomas_secundarios:
                    sintomas_secundarios.append(sintoma)

    df["numSintomas"] = df[
        [
            "distúrbios olfativos",
            "distúrbios gustativos",
            "outros",
            "dor de garganta",
            "dor de cabeça",
            "dispneia",
            "febre",
            "tosse",
            "coriza",
            "dificuldade de respirar",
        ]
    ].sum(axis=1)
    retained_columns = (
        [
            "idade",
            "sexo",
            "racaCor",
            "profissionalSeguranca",
            "profissionalSaude",
            "municipioNotificacao",
            "municipio",
            "totalTestesRealizados",
            "dataNotificacao",
            "dataInicioSintomas",
            "numSintomas",
        ]
        + [
            "distúrbios olfativos",
            "distúrbios gustativos",
            "outros",
            "dor de garganta",
            "dor de cabeça",
            "dispneia",
            "febre",
            "tosse",
            "coriza",
            "dificuldade de respirar",
        ]
        + ["classificacaoFinal"]
    )
    df = df[retained_columns]

    return df
