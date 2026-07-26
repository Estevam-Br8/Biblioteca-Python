import os
import glob
import pandas as pd
import numpy as np
from pathlib import Path

def run_etl():
    script_dir = Path(__file__).resolve().parent
    project_root = script_dir.parent
    
    raw_dir = project_root / "dados" / "base"
    processed_dir = project_root / "dados" / "processados"
    processed_dir.mkdir(parents=True, exist_ok=True)
    
    # Localiza o arquivo CSV bruto baixado
    csv_files = list(raw_dir.glob("*.csv"))
    if not csv_files:
        raise FileNotFoundError(f"Nenhum arquivo CSV encontrado em: {raw_dir}. Execute o script 01_import_api.py primeiro.")
    
    raw_file = csv_files[0]
    print(f"📖 Lendo arquivo bruto: {raw_file.name}")
    df = pd.read_csv(raw_file)
    
    # 1. Padronização de nomes de colunas
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
    
    # 2. Limpeza de dados
    df = df.dropna().drop_duplicates()
    
    # 3. Engenharia de atributos (Exemplo com faixa etária)
    if 'age' in df.columns:
        df['age_group'] = np.select(
            [df['age'] < 30, df['age'].between(30, 59), df['age'] >= 60],
            ['Jovem', 'Adulto', 'Sênior'],
            default='Não Informado'
        )
    
    # 4. Salvar dados processados em Parquet
    output_path = processed_dir / "blood_test_cleaned.parquet"
    df.to_parquet(output_path, index=False)
    print(f"✅ ETL concluído! Arquivo gerado em: {output_path}")

if __name__ == "__main__":
    run_etl()