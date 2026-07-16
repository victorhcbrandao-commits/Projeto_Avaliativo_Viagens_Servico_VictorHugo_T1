"""Fase 1 - Extração e carga na camada Raw."""
import zipfile
from pathlib import Path
import gdown
import pandas as pd
from sqlalchemy import text
from banco import criar_engine, executar_sql_arquivo, testar_conexao
from config import BASE_DIR, RAW_DIR, ZIP_PATH, DRIVE_FILE_ID, CSV_CONFIG


def baixar_zip_google_drive() -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    if ZIP_PATH.exists():
        print(f"ZIP encontrado: {ZIP_PATH}")
        return
    if not DRIVE_FILE_ID:
        raise FileNotFoundError("ZIP não encontrado. Coloque viagens_2025_6meses.zip em data/raw/ ou configure DRIVE_FILE_ID no .env.")
    url = f"https://drive.google.com/uc?id={DRIVE_FILE_ID}"
    print("Baixando ZIP do Google Drive...")
    gdown.download(url, str(ZIP_PATH), quiet=False)


def extrair_zip() -> Path:
    pasta_extraida = RAW_DIR / "extraido"
    pasta_extraida.mkdir(parents=True, exist_ok=True)
    print("Extraindo arquivos CSV...")
    with zipfile.ZipFile(ZIP_PATH, "r") as zip_ref:
        zip_ref.extractall(pasta_extraida)
    return pasta_extraida


def validar_csvs_extraidos(pasta_extraida: Path) -> None:
    esperados = [cfg["arquivo"] for cfg in CSV_CONFIG.values()]
    faltantes = [arquivo for arquivo in esperados if not (pasta_extraida / arquivo).exists()]
    if faltantes:
        raise FileNotFoundError(f"Arquivos CSV não encontrados: {faltantes}")


def truncar_raw() -> None:
    engine = criar_engine()
    with engine.begin() as conn:
        conn.execute(text("TRUNCATE TABLE raw_trecho, raw_passagem, raw_pagamento, raw_viagem RESTART IDENTITY;"))


def carregar_csv_raw(pasta_extraida: Path) -> None:
    engine = criar_engine()
    for _, cfg in CSV_CONFIG.items():
        caminho_csv = pasta_extraida / cfg["arquivo"]
        tabela = cfg["tabela_raw"]
        mapa_colunas = cfg["colunas"]
        print(f"Carregando {cfg['arquivo']} -> {tabela}")
        total = 0
        for chunk in pd.read_csv(caminho_csv, sep=";", encoding="latin1", dtype=str, chunksize=50000, keep_default_na=False):
            chunk = chunk.rename(columns=mapa_colunas)
            faltantes = [col for col in mapa_colunas.values() if col not in chunk.columns]
            if faltantes:
                raise KeyError(f"Colunas esperadas não encontradas em {cfg['arquivo']}: {faltantes}")
            chunk = chunk[list(mapa_colunas.values())]
            chunk.to_sql(tabela, engine, if_exists="append", index=False, method="multi", chunksize=5000)
            total += len(chunk)
        print(f"{tabela}: {total:,} registros carregados")


def main() -> None:
    print("=" * 70)
    print("FASE 1 - EXTRAÇÃO E CAMADA RAW")
    print("=" * 70)
    testar_conexao()
    print("Criando tabelas Raw e Silver...")
    executar_sql_arquivo(str(BASE_DIR / "0_criar_banco.sql"))
    baixar_zip_google_drive()
    pasta_extraida = extrair_zip()
    validar_csvs_extraidos(pasta_extraida)
    truncar_raw()
    carregar_csv_raw(pasta_extraida)
    print("Camada Raw criada com sucesso.")


if __name__ == "__main__":
    main()
