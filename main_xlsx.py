import sys
import os
import pandas as pd
from mapeamento import identificar_empresa, carregar_mapeamento, carregar_formatos
from processador import transformar_dataframe
from formatador_xlsxwriter import salvar_com_formatacao_xlsxwriter


def main(path_in, path_out, map_file):
    # 1) Leitura e normalização dos headers
    df_input = pd.read_excel(path_in, engine="openpyxl", header=0, dtype=str)
    df_input.columns = (
        df_input.columns
        .str.normalize("NFKC")
        .str.strip()
    )

    # 2) Identificar empresa e carregar map e formatos
    empresa = identificar_empresa(path_in)
    mapeamento = carregar_mapeamento(map_file, empresa)
    formatos = carregar_formatos(map_file)

    # 3) Transformação pura
    df_saida = transformar_dataframe(df_input, mapeamento)

    # TESTE: salvar sem formatação
    df_saida.to_excel("Coplacana_Original_Formatado_SIMPLES.xlsx", index=False)
    print("Arquivo simples salvo.")

    # 4) Gravação com formatação XlsxWriter
    salvar_com_formatacao_xlsxwriter(df_saida, path_out, formatos)

    # 5) Mensagem final
    ent = os.path.basename(path_in)
    sai = os.path.basename(path_out)
    print(f"✅ Concluído: {ent} → {sai}")


if __name__ == "__main__":
    _, inp, out, mp = sys.argv
    main(inp, out, mp)
