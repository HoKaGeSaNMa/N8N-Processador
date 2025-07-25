import sys
import os
import pandas as pd
from mapeamento import identificar_empresa, carregar_mapeamento, carregar_formatos
from processador_txt import transformar_dataframe
from formatador_xlsxwriter import salvar_com_formatacao_xlsxwriter
import chardet


def detectar_codificacao(path):
    with open(path, "rb") as f:
        return chardet.detect(f.read())["encoding"]


def ler_txt_explicitamente(path, encoding):
    with open(path, 'r', encoding=encoding) as file:
        linhas = file.readlines()

    # Extrair o cabeçalho de maneira extremamente explícita
    header = linhas[0].strip().split('|')
    linhas_dados = linhas[1:]

    dados = []
    for linha in linhas_dados:
        valores = linha.strip().split('|')
        # Completa colunas faltantes com valores vazios
        valores += [''] * (len(header) - len(valores))
        dados.append(valores[:len(header)])  # Garante tamanho exato

    return pd.DataFrame(dados, columns=header)


def main(path_txt, path_out, map_file):
    encoding = detectar_codificacao(path_txt)

    # Ler explicitamente (não usa pandas diretamente para leitura inicial)
    df_input = ler_txt_explicitamente(path_txt, encoding)
    df_input.columns = df_input.columns.str.normalize("NFKC").str.strip()

    empresa = identificar_empresa(path_txt)
    mapeamento = carregar_mapeamento(map_file, empresa)
    formatos = carregar_formatos(map_file)

    df_saida = transformar_dataframe(df_input, mapeamento)

    salvar_com_formatacao_xlsxwriter(df_saida, path_out, formatos)

    print(
        f"✅ Concluído com sucesso: {os.path.basename(path_txt)} → {os.path.basename(path_out)}")


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Uso: python main_txt.py <arquivo.txt> <arquivo_saida.xlsx> <arquivo_mapeamento.xlsx>")
        sys.exit(1)
    main(sys.argv[1], sys.argv[2], sys.argv[3])
