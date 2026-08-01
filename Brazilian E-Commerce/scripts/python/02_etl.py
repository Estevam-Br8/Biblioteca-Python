import sqlite3
from pathlib import Path
import pandas as pd
import numpy as np

# ==============================================================================
# 1. MAPEAMENTO DE PASTAS (PATHLIB)
# ==============================================================================
DIRETORIO_SCRIPT = Path(__file__).resolve().parent
RAIZ_PROJETO = DIRETORIO_SCRIPT.parent.parent

PASTA_BASE = RAIZ_PROJETO / "dados" / "base"
PASTA_PROCESSADOS = RAIZ_PROJETO / "dados" / "processados"

# Garante que a pasta de destino exista
PASTA_PROCESSADOS.mkdir(parents=True, exist_ok=True)

# Definição dos caminhos dos arquivos finais
caminho_banco = PASTA_PROCESSADOS / "ecommerce_analytics.db"
caminho_parquet = PASTA_PROCESSADOS / "vendas_processadas.parquet"

def executar_etl():
    # ==========================================================================
    # 2. VERIFICAÇÃO SE O PROCESSO DE ETL JÁ FOI REALIZADO
    # ==========================================================================
    if caminho_banco.exists():
        print(f"⚠️  O arquivo {caminho_banco.name} já existe! Parece que o processo de ETL já foi feito.")
        print("-" * 65)
        print("   📄 Arquivo encontrado em: dados/processados/ecommerce_analytics.db")
        print("-" * 65)
        
        print("\nEscolha uma das opções abaixo:")
        print("[S] Substituir (refazer o ETL e atualizar o banco SQL)")
        print("[C] Cancelar operação")
        
        resposta = input("\n👉 Digite sua opção (S/C): ").strip().upper()
        
        if resposta == 'S':
            print("\n🔄 Iniciando reprocessamento dos dados...")
        else:
            print("\n❌ Operação cancelada pelo usuário. O banco de dados SQLite não foi alterado.")
            return  # Encerra a função sem reprocessar nada

    print("\n🚀 Iniciando o ETL para Varejo...")

    # ==========================================================================
    # 3. LEITURA DOS ARQUIVOS BRUTOS (.CSV)
    # ==========================================================================
    try:
        print("📥 Lendo os arquivos CSV brutos...")
        df_orders = pd.read_csv(PASTA_BASE / "olist_orders_dataset.csv")
        df_items = pd.read_csv(PASTA_BASE / "olist_order_items_dataset.csv")
        df_products = pd.read_csv(PASTA_BASE / "olist_products_dataset.csv")
        df_payments = pd.read_csv(PASTA_BASE / "olist_order_payments_dataset.csv")
        df_customers = pd.read_csv(PASTA_BASE / "olist_customers_dataset.csv")
        df_translation = pd.read_csv(PASTA_BASE / "product_category_name_translation.csv")
    except FileNotFoundError as e:
        print(f"❌ Erro: Arquivo CSV não encontrado na pasta 'dados/base'.")
        print("💡 Execute primeiro o script '01_import_api.py' para baixar os dados!")
        return

    # ==========================================================================
    # 4. TRATAMENTO E JUNÇÃO DOS DADOS (JOIN / MERGE)
    # ==========================================================================
    print("🔄 Cruzando as tabelas e tratando valores...")

    # A) Traduzir categorias de produtos
    df_products = pd.merge(df_products, df_translation, on="product_category_name", how="left")

    # B) Juntar Pedidos + Itens do Pedido + Produtos + Clientes
    df_merged = pd.merge(df_orders, df_items, on="order_id", how="inner")
    df_merged = pd.merge(df_merged, df_products, on="product_id", how="left")
    df_merged = pd.merge(df_merged, df_customers, on="customer_id", how="left")

    # C) Pegar o tipo de pagamento principal por pedido
    df_payments_agg = df_payments.groupby("order_id").agg({
        "payment_type": "first",
        "payment_installments": "max"
    }).reset_index()

    df_final = pd.merge(df_merged, df_payments_agg, on="order_id", how="left")

    # D) Tratar datas (converter texto para data real)
    df_final["order_purchase_timestamp"] = pd.to_datetime(df_final["order_purchase_timestamp"])
    df_final["order_delivered_customer_date"] = pd.to_datetime(df_final["order_delivered_customer_date"])

    # E) Criar coluna de Tempo de Entrega (em dias)
    df_final["dias_para_entrega"] = (
        df_final["order_delivered_customer_date"] - df_final["order_purchase_timestamp"]
    ).dt.days

    # F) Regra estilo Fast Shop: Faixa de Preço do Produto (Entrada, Intermediário, Premium)
    condicoes = [
        (df_final["price"] < 100),
        (df_final["price"] >= 100) & (df_final["price"] <= 500),
        (df_final["price"] > 500)
    ]
    escolhas = ["Entrada", "Intermediário", "Premium"]
    df_final["faixa_preco"] = np.select(condicoes, escolhas, default="Outros")

    # G) Selecionar e Renomear colunas para português limpo (padrão SQL)
    colunas_finais = {
        "order_id": "id_pedido",
        "customer_state": "estado_cliente",
        "customer_city": "cidade_cliente",
        "order_status": "status_pedido",
        "order_purchase_timestamp": "data_compra",
        "dias_para_entrega": "dias_para_entrega",
        "product_category_name_english": "categoria_produto",
        "price": "preco_produto",
        "freight_value": "valor_frete",
        "payment_type": "metodo_pagamento",
        "payment_installments": "num_parcelas",
        "faixa_preco": "faixa_preco"
    }

    df_final = df_final[list(colunas_finais.keys())].rename(columns=colunas_finais)

    # Preencher nulos nas categorias com "outros"
    df_final["categoria_produto"] = df_final["categoria_produto"].fillna("outros")

    # Remover linhas sem data de entrega
    df_final = df_final.dropna(subset=["dias_para_entrega"])

    caminho_csv = PASTA_PROCESSADOS / "vendas_processadas.csv"
    df_final.to_csv(caminho_csv, index=False, encoding="utf-8")
    print(f"📄 Arquivo CSV limpo salvo em: {caminho_csv.name}")

    # ==========================================================================
    # 5. EXPORTAÇÃO 1: FICHEIRO PARQUET
    # ==========================================================================
    df_final.to_parquet(caminho_parquet, index=False)
    print(f"📦 Arquivo Parquet salvo em: {caminho_parquet.name}")

    # ==========================================================================
    # 6. EXPORTAÇÃO 2: BANCO DE DADOS SQLITE (PARA O DBEAVER)
    # ==========================================================================
    print(f"🛢️ Atualizando o banco SQL SQLite em: {caminho_banco.name}...")

    # Abre a conexão com o banco SQLite e substitui/grava a tabela 'tb_vendas'
    conn = sqlite3.connect(caminho_banco)
    df_final.to_sql("tb_vendas", conn, if_exists="replace", index=False)
    conn.close()

    print("\n✅ ETL concluído com sucesso!")
    print(f"📊 Total de registros gravados: {len(df_final):,} linhas")
    print(f"🎯 Tabela pronta no SQLite: 'tb_vendas'")

# ==============================================================================
# 7. EXECUÇÃO
# ==============================================================================
if __name__ == "__main__":
    executar_etl()