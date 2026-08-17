import sqlite3
import sys
from pathlib import Path
import pandas as pd

# 1. CAMINHOS DOS ARQUIVOS
pasta_base = Path(__file__).resolve().parent.parent / "base"
origem_csv = pasta_base / "Loan Dataset.csv"
destino_csv = pasta_base / "loan_approval_limpo.csv"
destino_db = pasta_base / "loan_approval.db"

if not origem_csv.exists():
    print(f"[ERRO] Arquivo não encontrado: {origem_csv}")
    sys.exit(1)

print("[1/3] Extraindo dados da base bruta...")
df = pd.read_csv(origem_csv)

# ==============================================================================
print("[2/3] Transformando e limpando dados essenciais...")

# Padroniza nomes das colunas: minúsculo, sem espaços extras e com underline
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

# Remove registros duplicados
df = df.drop_duplicates()

# Filtro de segurança para idade (se a coluna existir na base)
if "person_age" in df.columns:
    df = df[(df["person_age"] >= 18) & (df["person_age"] <= 100)]
    df["faixa_etaria"] = pd.cut(
        df["person_age"],
        bins=[17, 25, 35, 50, 100],
        labels=["18-25 anos", "26-35 anos", "36-50 anos", "50+ anos"],
    ).astype(str)

# Cria Faixa de Score de Crédito (busca 'cibil_score' ou 'credit_score')
col_score = next(
    (col for col in ["cibil_score", "credit_score"] if col in df.columns), None
)
if col_score:
    df["faixa_score"] = pd.cut(
        df[col_score],
        bins=[0, 580, 700, 1000],
        labels=[
            "Alto Risco (<580)",
            "Médio Risco (580-700)",
            "Baixo Risco (>700)",
        ],
    ).astype(str)

# Traduz o Status do Empréstimo para um texto claro no Power BI
if "loan_status" in df.columns:
    df["status_rotulo"] = (
        df["loan_status"]
        .replace(
            {
                1: "Aprovado / Adimplente",
                0: "Negado / Inadimplente",
                "Approved": "Aprovado / Adimplente",
                "Rejected": "Negado / Inadimplente",
            }
        )
        .astype(str)
    )

# ==============================================================================
print("[3/3] Exportando bases processadas...")

# 1. Salva o CSV limpo para usar no Power BI
df.to_csv(destino_csv, index=False, encoding="utf-8-sig")

# 2. Salva o banco SQLite (.db) para usar no DBeaver
with sqlite3.connect(destino_db) as conexao:
    df.to_sql("carteira_credito", conexao, if_exists="replace", index=False)

print("\n" + "=" * 50)
print(f"SUCESSO! Base tratada com {len(df):,} linhas.")
print(f" -> CSV Power BI: {destino_csv.name}")
print(f" -> DB DBeaver:   {destino_db.name}")
print("=" * 50 + "\n")