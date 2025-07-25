import os
import sys
import pandas as pd
import chardet


def detectar_codificacao(path):
    with open(path, "rb") as f:
        data = f.read()
    return chardet.detect(data)["encoding"]


def main(txt_path):
    enc = detectar_codificacao(txt_path)

    # Leitura direta do TXT original
    df = pd.read_csv(txt_path, sep='|', encoding=enc, dtype=str,
                     keep_default_na=False, engine="python")

    # Salva o CSV corretamente
    csv_path = os.path.splitext(txt_path)[0] + ".csv"
    df.to_csv(csv_path, index=False, sep=",", encoding="utf-8-sig")

    print(f"✅ CSV gerado com sucesso: {csv_path}")
    sys.exit(0)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python txt_para_csv.py <arquivo.txt>")
        sys.exit(1)
    main(sys.argv[1])
