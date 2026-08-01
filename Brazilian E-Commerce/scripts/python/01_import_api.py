import shutil
from pathlib import Path
import kagglehub

# ==============================================================================
# 1. GERENCIAMENTO DE CAMINHOS COM PATHLIB
# ==============================================================================
DIRETORIO_SCRIPT = Path(__file__).resolve().parent
RAIZ_PROJETO = DIRETORIO_SCRIPT.parent.parent
PASTA_DESTINO = RAIZ_PROJETO / "dados" / "base"

# Garante que a pasta 'dados/base' existe
PASTA_DESTINO.mkdir(parents=True, exist_ok=True)

# ==============================================================================
# 2. INGESTÃO DE DADOS COM VERIFICAÇÃO DE FICHEIROS
# ==============================================================================
DATASET_SLUG = "olistbr/brazilian-ecommerce"

def verificar_e_executar_ingestao():
    """
    Verifica se já existem arquivos na pasta 'dados/base'.
    Se existirem, mostra a mensagem informando os arquivos encontrados
    e exibe as opções para o usuário.
    """
    # Procura por arquivos existentes na pasta dados/base
    arquivos_existentes = list(PASTA_DESTINO.glob("*"))
    
    # Se existirem arquivos, exibe a mensagem personalizada
    if arquivos_existentes:
        print("⚠️  Parece que a importação já foi feita! Encontrei os seguintes arquivos:")
        print("-" * 60)
        for f in arquivos_existentes:
            if f.is_file():
                print(f"   📄 {f.name}")
        print("-" * 60)
        
        print("\nEscolha uma das opções abaixo:")
        print("[S] Substituir tudo (apagar arquivos atuais e refazer importação)")
        print("[C] Cancelar operação")
        
        resposta = input("\n👉 Digite sua opção (S/C): ").strip().upper()
        
        if resposta == 'S':
            print("\n🔄 Apagando arquivos antigos para refazer a importação...")
            for f in arquivos_existentes:
                if f.is_file():
                    f.unlink()  # Remove o arquivo antigo
            print("🧹 Pasta limpa com sucesso! Iniciando download...\n")
        else:
            print("\n❌ Operação cancelada pelo usuário. Nenhum arquivo foi alterado.")
            return  # Encerra a função sem fazer download

    # ==========================================================================
    # EXECUÇÃO DA IMPORTAÇÃO (DOWNLOAD E CÓPIA)
    # ==========================================================================
    print(f"🚀 Iniciando download via kagglehub: {DATASET_SLUG}...")
    
    try:
        # 1. Faz o download com a biblioteca kagglehub
        path_temp = kagglehub.dataset_download(DATASET_SLUG)
        pasta_origem = Path(path_temp)
        
        print(f"📦 Arquivos baixados para a pasta temporária: {pasta_origem}")
        print(f"🔄 Copiando arquivos para a pasta do projeto: {PASTA_DESTINO}")
        
        # 2. Copia os arquivos para a pasta dados/base
        for arquivo in pasta_origem.glob("*"):
            if arquivo.is_file():
                destino_final = PASTA_DESTINO / arquivo.name
                shutil.copy2(arquivo, destino_final)
                print(f"   📄 Copiado: {arquivo.name}")
                
        print("\n✅ Importação concluída com sucesso!")
        print(f"📂 Arquivos disponíveis em: {PASTA_DESTINO}")

    except Exception as e:
        print(f"❌ Erro durante o download ou cópia dos dados: {e}")

# ==============================================================================
# 3. EXECUÇÃO DO SCRIPT
# ==============================================================================
if __name__ == "__main__":
    verificar_e_executar_ingestao()