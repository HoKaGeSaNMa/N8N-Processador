import pandas as pd
from collections import OrderedDict
import os


def identificar_empresa(path_arquivo: str) -> str:
    base = os.path.splitext(os.path.basename(path_arquivo))[0]
    return base.split("_")[0].strip()


def carregar_mapeamento(path_map: str, nome_empresa: str) -> OrderedDict:
    df = pd.read_excel(path_map, sheet_name="COLUMN_MAP", dtype=str).fillna("")
    df["__empresa_norm"] = df["Empresa"].str.strip().str.lower()
    linha = df[df["__empresa_norm"] == nome_empresa.lower()]
    if linha.empty:
        raise ValueError(
            f"Empresa '{nome_empresa}' não encontrada em COLUMN_MAP")
    row = linha.iloc[0]

    cols = [c for c in df.columns if c not in ("Empresa", "__empresa_norm")]
    mapping = OrderedDict()
    for dest in cols:
        orig = row[dest].strip()
        mapping[dest] = orig if orig else None
    return mapping


def carregar_formatos(path_map: str) -> dict:
    df = pd.read_excel(path_map, sheet_name="COLUMN_CONFIG",
                       dtype=str).fillna("")
    return dict(zip(df["Coluna"].str.strip(), df["Tipo"].str.strip()))
