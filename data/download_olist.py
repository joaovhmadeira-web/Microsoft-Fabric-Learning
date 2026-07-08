"""
Download e preparação do subconjunto do dataset Olist para o projeto de migração Fabric.

Baixa o dataset público "olistbr/brazilian-ecommerce" do Kaggle, mantém apenas as
6 tabelas em escopo e gera:
  - data/raw/     -> CSVs completos das 6 tabelas (NÃO versionar)
  - data/sample/  -> amostra pequena de cada tabela (pode versionar p/ inspeção)

Pré-requisitos:
  pip install kaggle pandas
  Credenciais do Kaggle em ~/.kaggle/kaggle.json  (ou %USERPROFILE%\\.kaggle\\kaggle.json no Windows)
  https://www.kaggle.com/docs/api

Uso:
  python download_olist.py                # baixa via Kaggle API
  python download_olist.py --zip caminho.zip   # usa um zip já baixado manualmente
  python download_olist.py --sample-rows 500   # tamanho da amostra (default 1000)
"""
from __future__ import annotations

import argparse
import sys
import zipfile
from pathlib import Path

# Mapa: nome lógico no projeto -> arquivo no dataset Kaggle
TABLES = {
    "orders": "olist_orders_dataset.csv",
    "order_items": "olist_order_items_dataset.csv",
    "order_payments": "olist_order_payments_dataset.csv",
    "customers": "olist_customers_dataset.csv",
    "sellers": "olist_sellers_dataset.csv",
    "products": "olist_products_dataset.csv",
}

KAGGLE_DATASET = "olistbr/brazilian-ecommerce"
HERE = Path(__file__).resolve().parent
RAW_DIR = HERE / "raw"
SAMPLE_DIR = HERE / "sample"


def download_zip_via_kaggle(dest: Path) -> Path:
    """Baixa o dataset como zip usando a Kaggle CLI/API."""
    try:
        from kaggle.api.kaggle_api_extended import KaggleApi
    except ImportError:
        sys.exit(
            "Pacote 'kaggle' nao instalado. Rode: pip install kaggle\n"
            "Ou baixe o zip manualmente e use --zip caminho.zip"
        )
    api = KaggleApi()
    api.authenticate()
    print(f"Baixando {KAGGLE_DATASET} do Kaggle...")
    api.dataset_download_files(KAGGLE_DATASET, path=str(dest), unzip=False, quiet=False)
    zips = list(dest.glob("*.zip"))
    if not zips:
        sys.exit("Download concluido mas nenhum .zip encontrado.")
    return zips[0]


def extract_scoped_tables(zip_path: Path) -> None:
    """Extrai apenas as 6 tabelas em escopo do zip para RAW_DIR, renomeando."""
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    wanted = {v: k for k, v in TABLES.items()}  # arquivo kaggle -> nome logico
    with zipfile.ZipFile(zip_path) as zf:
        names = set(zf.namelist())
        missing = [f for f in wanted if f not in names]
        if missing:
            sys.exit(f"Arquivos esperados nao encontrados no zip: {missing}")
        for kaggle_file, logical in wanted.items():
            out = RAW_DIR / f"{logical}.csv"
            with zf.open(kaggle_file) as src, open(out, "wb") as dst:
                dst.write(src.read())
            print(f"  raw/{logical}.csv")


def make_samples(sample_rows: int) -> None:
    """Gera amostras pequenas (head) de cada tabela para inspeção/versionamento."""
    try:
        import pandas as pd
    except ImportError:
        print("pandas nao instalado; pulando geracao de amostras.")
        return
    SAMPLE_DIR.mkdir(parents=True, exist_ok=True)
    for logical in TABLES:
        src = RAW_DIR / f"{logical}.csv"
        if not src.exists():
            continue
        df = pd.read_csv(src, nrows=sample_rows)
        df.to_csv(SAMPLE_DIR / f"{logical}.csv", index=False)
        print(f"  sample/{logical}.csv  ({len(df)} linhas)")


def main() -> None:
    ap = argparse.ArgumentParser(description="Prepara dados Olist para o projeto Fabric.")
    ap.add_argument("--zip", type=Path, help="Usa um zip ja baixado em vez da Kaggle API.")
    ap.add_argument("--sample-rows", type=int, default=1000, help="Linhas por amostra (default 1000).")
    ap.add_argument("--no-sample", action="store_true", help="Nao gerar amostras.")
    args = ap.parse_args()

    zip_path = args.zip if args.zip else download_zip_via_kaggle(HERE)
    if not zip_path.exists():
        sys.exit(f"Zip nao encontrado: {zip_path}")

    print("Extraindo tabelas em escopo...")
    extract_scoped_tables(zip_path)

    if not args.no_sample:
        print("Gerando amostras...")
        make_samples(args.sample_rows)

    print("\nOK. Suba os arquivos de data/raw/ como camada Bronze no Lakehouse.")


if __name__ == "__main__":
    main()
