# N8N-Processador

Projeto de automação de processamento de arquivos `.xlsx` e `.txt`, com base em mapeamento personalizado por empresa.

## 📁 Estrutura do projeto

- `monitor_pasta.py`: Monitora uma pasta e inicia o processamento automaticamente.
- `processador.py`: Processa os arquivos de entrada.
- `formatador_xlsxwriter.py` e `formatador_txt.py`: Formatam os arquivos segundo o mapeamento.
- `mapeamento_empresas.xlsx`: Define o layout por empresa.
- `main_*.py`: Entradas principais de execução.

## ⚙️ Requisitos

- Python 3.11
- pandas
- openpyxl
- xlsxwriter

## ▶️ Como usar

1. Execute `monitor_pasta.py`.
2. Coloque os arquivos da empresa na pasta `Entrada`.
3. O sistema irá formatar e salvar automaticamente.

## 🔍 Observações

- Todos os arquivos são validados com base na aba `COLUMN_CONFIG` do Excel de mapeamento.
- A estrutura foi otimizada para arquivos grandes (até 1 milhão de linhas).
