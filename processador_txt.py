import pandas as pd
import difflib

def transformar_dataframe(df_entrada: pd.DataFrame, mapeamento: dict) -> pd.DataFrame:
    lookup = {col.strip().lower(): col for col in df_entrada.columns}
    keys = list(lookup.keys())
    
    dados = {}
    for destino, origem in mapeamento.items():
        if origem:
            key = origem.strip().lower()

            # Tratamento para concatenação &&
            if "&&" in key:
                parts = [p.strip() for p in origem.split("&&")]
                series = [_match_fuzzy(df_entrada, lookup, p) for p in parts]
                dados[destino] = series[0].astype(str).str.strip() + " " + series[1].astype(str).str.strip()
                continue

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

        # Coluna vazia se nada encontrado
        dados[destino] = [""] * len(df_entrada)

    # Garante rigorosamente a ordem do mapeamento original
    df_final = pd.DataFrame({col: dados[col] for col in mapeamento.keys()})
    return df_final

def _match_fuzzy(df, lookup, origem):
    key = origem.strip().lower()
    keys = list(lookup.keys())
    match = difflib.get_close_matches(key, keys, n=1, cutoff=0.6)
    return df[lookup[match[0]]] if match else pd.Series([""] * len(df), index=df.index)
