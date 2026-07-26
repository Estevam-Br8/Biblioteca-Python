import pandas as pd
import numpy as np
from pathlib import Path

def analyze_data():
    script_dir = Path(__file__).resolve().parent
    project_root = script_dir.parent
    
    processed_file = project_root / "dados" / "processados" / "blood_test_cleaned.parquet"
    
    if not processed_file.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {processed_file}. Execute o script 02_etl.py primeiro.")
    
    print("📈 Carregando dados para análise...\n")
    df = pd.read_parquet(processed_file)
    
    # ----------------------------------------------------
    # 1. VISÃO GERAL DO PIPELINE
    # ----------------------------------------------------
    print("=" * 55)
    print("1. VISÃO GERAL DO DATASET")
    print("=" * 55)
    print(f"Total de Pacientes Analisados: {len(df):,}")
    print(f"Total de Atributos/Exames:    {len(df.columns)}")
    
    # ----------------------------------------------------
    # 2. PRINCIPAIS INDICADORES DE SAÚDE (MÉDIAS E DESVIOS)
    # ----------------------------------------------------
    print("\n" + "=" * 55)
    print("2. PRINCIPAIS INDICADORES CLÍNICOS (MÉDIA E MEDIANA)")
    print("=" * 55)
    
    # Seleciona apenas colunas numéricas de exames
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    
    if len(numeric_cols) > 0:
        summary = df[numeric_cols].agg(['mean', 'median', 'std', 'min', 'max']).T
        summary.columns = ['Média', 'Mediana', 'Desv. Padrão', 'Mínimo', 'Máximo']
        print(summary.round(2))
    
    # ----------------------------------------------------
    # 3. ANÁLISE POR GRUPOS (DEMOGRÁFICO)
    # ----------------------------------------------------
    if 'age_group' in df.columns:
        print("\n" + "=" * 55)
        print("3. DISTRIBUIÇÃO DEMOGRÁFICA POR FAIXA ETÁRIA")
        print("=" * 55)
        age_dist = df['age_group'].value_counts(normalize=True) * 100
        for group, pct in age_dist.items():
            print(f"• {group:<10}: {pct:.2f}%")

    if 'gender' in df.columns:
        print("\n" + "=" * 55)
        print("4. PROPORÇÃO POR GÊNERO")
        print("=" * 55)
        gender_dist = df['gender'].value_counts(normalize=True) * 100
        for gender, pct in gender_dist.items():
            print(f"• {gender:<10}: {pct:.2f}%")

    # ----------------------------------------------------
    # 4. CRUZAMENTO DE DADOS (INDICADORES CHAVE POR GRUPO)
    # ----------------------------------------------------
    # Caso existam exames específicos no dataset (ex: glucose, cholesterol)
    key_metrics = [col for col in ['glucose', 'cholesterol', 'hemoglobin', 'triglycerides'] if col in df.columns]
    
    if key_metrics and 'age_group' in df.columns:
        print("\n" + "=" * 55)
        print("5. MÉDIA DOS PRINCIPAIS EXAMES POR FAIXA ETÁRIA")
        print("=" * 55)
        grouped_metrics = df.groupby('age_group')[key_metrics].mean()
        print(grouped_metrics.round(2))

    print("\n" + "=" * 55)
    print("✅ Análise executiva concluída com sucesso!")
    print("=" * 55)

if __name__ == "__main__":
    analyze_data()