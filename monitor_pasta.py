import os
import time
from watchdog.observers import Observer
from watchdog.events import FileCreatedEvent, FileSystemEventHandler

# Descobre onde está este script e vai um nível acima (para Arquivos_N8N)
BASE_DIR = os.path.dirname(__file__)        # .../Arquivos_N8N/Main
ROOT_DIR = os.path.dirname(BASE_DIR)        # .../Arquivos_N8N

# Pastas fixas (já existem em ROOT_DIR)
INPUT_DIR = os.path.join(ROOT_DIR, "Entrada")
OUTPUT_DIR = os.path.join(ROOT_DIR, "Saida")
MAPPING = os.path.join(BASE_DIR, "mapeamento_empresas.xlsx")  # dentro de Main

# Scripts (dentro de Main)
MAIN_XLSX = os.path.join(BASE_DIR, "main_xlsx.py")
MAIN_TXT = os.path.join(BASE_DIR, "main_txt.py")
TXT_TO_CSV = os.path.join(BASE_DIR, "txt_para_csv.py")


class Handler(FileSystemEventHandler):
    def on_created(self, event):
        if not isinstance(event, FileCreatedEvent):
            return
        src = event.src_path
        name, ext = os.path.splitext(src.lower())
        base = os.path.basename(src)
        if base.startswith("~$"):
            return

        print(f"\n▶️ Detectado {ext.upper()}: {base}")
        # XLSX → main_xlsx.py
        if ext == ".xlsx":
            out = os.path.join(
                OUTPUT_DIR, f"{os.path.splitext(base)[0]}_Formatado.xlsx")
            print(f"🔄 Processando XLSX → {os.path.basename(out)}")
            os.system(f'python "{MAIN_XLSX}" "{src}" "{out}" "{MAPPING}"')

        # TXT → CSV + main_txt.py
        elif ext == ".txt":
            out = os.path.join(OUTPUT_DIR, f"{os.path.splitext(base)[0]}.xlsx")
            print(
                f"🔄 Processando TXT→XLSX diretamente: {os.path.basename(out)}")
            os.system(f'python "{MAIN_TXT}" "{src}" "{out}" "{MAPPING}"')

        # CSV → main_txt.py
        elif ext == ".csv":
            out = os.path.join(OUTPUT_DIR, f"{os.path.splitext(base)[0]}.xlsx")
            print(f"🔄 Processando CSV→XLSX: {os.path.basename(out)}")
            os.system(f'python "{MAIN_TXT}" "{src}" "{out}" "{MAPPING}"')


if __name__ == "__main__":
    print(f"📁 Monitorando pasta de entrada: {INPUT_DIR}")
    observer = Observer()
    observer.schedule(Handler(), INPUT_DIR, recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
