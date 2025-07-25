import pandas as pd
import xlsxwriter

def salvar_com_formatacao_txt(df, caminho_saida, formatos):
    with pd.ExcelWriter(caminho_saida, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Dados')
        workbook = writer.book
        worksheet = writer.sheets['Dados']

        for idx, col in enumerate(df.columns):
            max_len = max(
                df[col].astype(str).map(len).max(),
                len(col)
            ) + 2
            worksheet.set_column(idx, idx, max_len)

        header_format = workbook.add_format({
            'bold': True,
            'bg_color': '#DCE6F1',
            'border': 1
        })
        for col_num, value in enumerate(df.columns.values):
            worksheet.write(0, col_num, value, header_format)
