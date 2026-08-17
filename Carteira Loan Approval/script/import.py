import shutil
import sys
from pathlib import Path
import kagglehub

# 1. Define o caminho da pasta 'base'
pasta_base = Path(__file__).resolve().parent.parent / "base"
pasta_base.mkdir(parents=True, exist_ok=True)

# 2. Verifica se já existe algum arquivo .csv na pasta 'base'
arquivos_existentes = list(pasta_base.glob("*.csv"))

if arquivos_existentes:
    print("\n" + "=" * 70)
    print("[ATENÇÃO] Arquivo(s) já existente(s) na pasta 'base':")
    for arq in arquivos_existentes:
        print(f" -> Arquivo: {arq.name}")
        print(f"    Caminho: {arq}")
    print("=" * 70)

    print("\nO que você deseja fazer?")
    print(" [S] Substituir (baixar novamente do Kaggle e sobrescrever)")
    print(" [N] Cancelar   (manter o arquivo atual sem alterações)")

    resposta = input("\nDigite sua opção (s/n): ").strip().lower()

    if resposta not in ["s", "sim", "1"]:
        print("\n[INFO] Operação cancelada. O arquivo existente foi mantido intacto.\n")
        sys.exit()

    print("\n[INFO] Limpando arquivos antigos da pasta 'base'...")
    for arquivo in pasta_base.glob("*"):
        if arquivo.is_file():
            arquivo.unlink()
else:
    print("\n[INFO] Nenhum arquivo .csv encontrado na pasta 'base'. Iniciando importação...")

# 3. Baixa o dataset do Kaggle (force_download=True para garantir a versão atualizada)
print("[INFO] Baixando a base de dados via kagglehub...")
caminho_cache = kagglehub.dataset_download(
    "arbaaztamboli/loan-approval-dataset", force_download=True
)

# 4. Localiza o CSV baixado no cache e copia para a pasta 'base'
origem_csv = next(Path(caminho_cache).rglob("*.csv"), None)

if not origem_csv:
    raise FileNotFoundError("Nenhum arquivo .csv foi encontrado no download do Kaggle.")

destino_csv = pasta_base / origem_csv.name
shutil.copy(origem_csv, destino_csv)

# 5. Exibe os caminhos de origem e destino
print("\n" + "=" * 70)
print("[SUCESSO] Base de dados importada com êxito!")
print("=" * 70)
print(f" -> [ORIGEM - CACHE KAGGLE]:\n    {origem_csv}\n")
print(f" -> [DESTINO - PASTA DO PROJETO]:\n    {destino_csv}")
print("=" * 70 + "\n")