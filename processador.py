import pandas as pd
import difflib


def transformar_dataframe(df_entrada: pd.DataFrame, mapeamento: dict) -> pd.DataFrame:
    lookup = {col.strip().lower(): col for col in df_entrada.columns}
    keys = list(lookup.keys())
    dados = {}

    for destino, origem in mapeamento.items():
        if origem:
            key = origem.strip().lower()
            # Match exato
            if key in lookup:
                dados[destino] = df_entrada[lookup[key]]
                continue
            # Fuzzy match
            match = difflib.get_close_matches(key, keys, n=1, cutoff=0.6)
            if match:
                real = lookup[match[0]]
                dados[destino] = df_entrada[real]
                continue
        # Default: coluna vazia
        dados[destino] = [""] * len(df_entrada)
    return pd.DataFrame(dados)
