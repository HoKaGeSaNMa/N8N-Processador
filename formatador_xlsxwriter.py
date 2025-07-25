import pandas as pd

# Função para salvar DataFrame com formatação específica usando xlsxwriter


def salvar_com_formatacao_xlsxwriter(df, caminho_saida, formatos):
    # Ajuste de tipos antes de gravar
    for col, tipo in formatos.items():
        if col not in df.columns:
            continue

        if tipo in ("VALOR CONTABIL 2C", "VALOR CONTABIL 4C"):
            df[col] = pd.to_numeric(df[col], errors="coerce")

        elif tipo == "CODIGO NUMERICO":
            # Solução robusta: converte para float primeiro, depois Int64
            df[col] = pd.to_numeric(
                df[col], errors="coerce").round(0).astype("Int64")

        elif tipo == "DATA DD/MM/AAAA":
            df[col] = pd.to_datetime(
                df[col], format='%d/%m/%Y', dayfirst=True, errors="coerce")

        elif tipo == "DATA ANO NUMERICO":
            # Solução robusta também aqui:
            df[col] = pd.to_numeric(
                df[col], errors="coerce").round(0).astype("Int64")

        elif tipo in ("CODIGO ALFA-NUMERICO", "DESCRICAO", "DATA MES LITERAL"):
            df[col] = df[col].astype(str)

    with pd.ExcelWriter(caminho_saida, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False, sheet_name="Sheet1")
        wb = writer.book
        ws = writer.sheets["Sheet1"]

        estilos = {
            "CODIGO NUMERICO": wb.add_format({"num_format": "0"}),
            "CODIGO ALFA-NUMERICO": wb.add_format({"num_format": "@"}),
            "VALOR CONTABIL 2C": wb.add_format({"num_format": "#,##0.00"}),
            "VALOR CONTABIL 4C": wb.add_format({"num_format": "#,##0.0000"}),
            "DATA DD/MM/AAAA": wb.add_format({"num_format": "dd/mm/yyyy"}),
            "DATA ANO NUMERICO": wb.add_format({"num_format": "0"}),
            "DATA MES LITERAL": wb.add_format({"num_format": "@"}),
            "DESCRICAO": wb.add_format({"num_format": "@"}),
        }

        for idx, col in enumerate(df.columns):
            fmt = estilos.get(formatos.get(col, "DESCRICAO"))
            ws.set_column(idx, idx, 20, fmt)

    print(f"✅ Arquivo salvo com sucesso: {caminho_saida}")
