import os
from pathlib import Path
from kaggle.api.kaggle_api_extended import KaggleApi

def download_dataset():
    # Caminho do script atual
    script_dir = Path(__file__).resolve().parent
    # Pasta raiz do projeto (uma pasta acima de scripts)
    project_root = script_dir.parent
    
    # Pasta onde os dados brutos serão salvos: ../dados/raw
    raw_dir = project_root / "dados" / "base"
    raw_dir.mkdir(parents=True, exist_ok=True)
    
    dataset_name = "kantesti/global-blood-test-health-insights-2025-2026"
    
    print("🔄 Autenticando na API do Kaggle...")
    api = KaggleApi()
    api.authenticate()
    
    print(f"📥 Baixando dataset em: {raw_dir}")
    api.dataset_download_files(dataset_name, path=str(raw_dir), unzip=True)
    
    print("✅ Download concluído com sucesso!")

if __name__ == "__main__":
    download_dataset()