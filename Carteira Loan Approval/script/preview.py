import sys
from pathlib import Path
import pandas as pd

# 1. LOCALIZAÇÃO DO ARQUIVO BRUTO
pasta_base = Path(__file__).resolve().parent.parent / "base"
origem_csv = pasta_base / "Loan Dataset.csv"

if not origem_csv.exists():
    print(f"[ERRO] Arquivo não encontrado:\n -> {origem_csv}")
    print("Execute primeiro o script 'import.py' para baixar a base do Kaggle.")
    sys.exit(1)

# Configuração do Pandas para exibir mais colunas no terminal sem cortar
pd.set_option("display.max_columns", 20)
pd.set_option("display.width", 1000)

print("\n" + "=" * 70)
print("             RAIO-X INICIAL DA BASE DE EMPRÉSTIMOS")
print("=" * 70)

# 2. CARREGAMENTO DA BASE
df = pd.read_csv(origem_csv)

# 3. DIMENSÕES GERAIS
linhas, colunas = df.shape
print(f"\n[1. DIMENSÕES GERAIS]")
print(f" -> Total de Registros (Linhas):  {linhas:,}")
print(f" -> Total de Atributos (Colunas): {colunas}")

# 4. LISTA DE COLUNAS E VALORES NULOS
print("\n" + "-" * 70)
print("[2. ESTRUTURA DE COLUNAS E VALORES AUSENTES (MISSING VALUES)]")
print("-" * 70)

resumo_nulos = pd.DataFrame({
    "Tipo de Dado": df.dtypes,
    "Valores Nulos": df.isnull().sum(),
    "% Nulos": (df.isnull().sum() / len(df) * 100).round(2)
})
print(resumo_nulos.to_string())

# 5. RESUMO ESTATÍSTICO DAS COLUNAS NUMÉRICAS
print("\n" + "-" * 70)
print("[3. RESUMO ESTATÍSTICO (NUMÉRICOS)]")
print("-" * 70)
# Formata números float com duas casas decimais para facilitar a leitura
pd.set_option("display.float_format", lambda x: "%.2f" % x)
print(df.describe().T[["count", "mean", "min", "50%", "max"]].rename(
    columns={"50%": "mediana"}
))

# 6. PRÉVIA REAL DA TABELA (TOP 5 LINHAS)
print("\n" + "-" * 70)
print("[4. PRÉVIA DOS DADOS - PRIMEIRAS 5 LINHAS (HEAD)]")
print("-" * 70)
print(df.head(5))

print("\n" + "=" * 70)
print("[DIAGNÓSTICO CONCLUÍDO] Pronto para validar as regras do ETL!")
print("=" * 70 + "\n")