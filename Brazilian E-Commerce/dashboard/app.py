import sqlite3
from pathlib import Path
import pandas as pd
import plotly.express as px
import streamlit as st

# ==============================================================================
# 1. CONFIGURAÇÃO DA PÁGINA E ESTILOS
# ==============================================================================
st.set_page_config(
    page_title="Brazilian E-Commerce Analytics",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded",
)


# Função para injetar o arquivo CSS
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


# Tenta carregar o CSS (style.css na mesma pasta)
try:
    local_css(Path(__file__).parent / "style.css")
except FileNotFoundError:
    pass


# ==============================================================================
# 2. CONEXÃO COM BANCO DE DADOS (CACHE DE ALTA PERFORMANCE)
# ==============================================================================
@st.cache_data
def carregar_dados():
    """Conecta no SQLite gerado pelo ETL e carrega os dados processados."""
    diretorio_atual = Path(__file__).resolve().parent
    caminho_banco = (
        diretorio_atual.parent / "dados" / "processados" / "ecommerce_analytics.db"
    )

    conn = sqlite3.connect(caminho_banco)
    query = """
        SELECT 
            id_pedido,
            estado_cliente,
            data_compra,
            dias_para_entrega,
            categoria_produto,
            preco_produto,
            valor_frete,
            faixa_preco,
            num_parcelas
        FROM tb_vendas
    """
    try:
        df = pd.read_sql_query(query, conn)
    except Exception:
        # Fallback de segurança caso a tabela antiga não tenha 'num_parcelas'
        query_fallback = """
            SELECT 
                id_pedido,
                estado_cliente,
                data_compra,
                dias_para_entrega,
                categoria_produto,
                preco_produto,
                valor_frete,
                faixa_preco
            FROM tb_vendas
        """
        df = pd.read_sql_query(query_fallback, conn)
        df["num_parcelas"] = 1
    finally:
        conn.close()

    df["data_compra"] = pd.to_datetime(df["data_compra"])
    df["ano_mes"] = df["data_compra"].dt.to_period("M").astype(str)

    # Garantia de não haver valores nulos nas parcelas
    if "num_parcelas" not in df.columns:
        df["num_parcelas"] = 1
    else:
        df["num_parcelas"] = df["num_parcelas"].fillna(1)

    return df


df = carregar_dados()

# ==============================================================================
# 3. BARRA LATERAL (FILTROS EXECUTIVOS)
# ==============================================================================
with st.sidebar:
    st.markdown("### 🎛️ Filtros de Análise")
    st.markdown("---")

    faixas_disponiveis = df["faixa_preco"].unique().tolist()
    faixa_selecionada = st.multiselect(
        "Faixa de Preço:",
        options=faixas_disponiveis,
        default=faixas_disponiveis,
    )

    top_estados = df["estado_cliente"].value_counts().head(10).index.tolist()
    estado_selecionado = st.multiselect(
        "Estado do Cliente:",
        options=top_estados,
        default=top_estados[:5],
    )

    st.markdown("---")
    st.caption("⚡ Dados atualizados automaticamente via pipeline ETL.")

# Aplicando filtros no DataFrame
df_filtrado = df[
    (df["faixa_preco"].isin(faixa_selecionada))
    & (df["estado_cliente"].isin(estado_selecionado))
]

# ==============================================================================
# 4. CABEÇALHO DO APLICATIVO
# ==============================================================================
st.markdown("## 🛍️ Executive E-Commerce Dashboard")
st.markdown(
    "<p style='color: #64748b; margin-top: -10px;'>Acompanhamento de performance de vendas e nível de serviço logístico.</p>",
    unsafe_allow_html=True,
)
st.markdown("---")

# ==============================================================================
# 5. SEÇÃO DE KPIS (DARK MODE + MÉTRICAS EXECUTIVAS)
# ==============================================================================
# 1. Função de formatação para números compactos (Ex: 9.773.989 -> 9,8M)
def formatar_numero(valor, prefixo=""):
    if valor >= 1_000_000:
        return f"{prefixo}{valor / 1_000_000:.1f}M".replace(".", ",")
    elif valor >= 1_000:
        return f"{prefixo}{valor / 1_000:.1f}K".replace(".", ",")
    else:
        return (
            f"{prefixo}{valor:,.2f}"
            .replace(",", "X")
            .replace(".", ",")
            .replace("X", ".")
        )


# 2. Cálculos Principais
receita_total = df_filtrado["preco_produto"].sum()
total_pedidos = df_filtrado["id_pedido"].nunique()
ticket_medio = receita_total / total_pedidos if total_pedidos > 0 else 0
tempo_medio_entrega = df_filtrado["dias_para_entrega"].mean()

# 3. Cálculos Complementares (com proteção contra divisão por zero e colunas ausentes)
frete_total = df_filtrado["valor_frete"].sum()
frete_pct = (frete_total / receita_total) * 100 if receita_total > 0 else 0

total_produtos = len(df_filtrado)
itens_por_pedido = total_produtos / total_pedidos if total_pedidos > 0 else 0

if "num_parcelas" in df_filtrado.columns:
    parcelas_media = df_filtrado["num_parcelas"].mean()
else:
    parcelas_media = 1.0

entrega_rapida_pct = (
    (df_filtrado["dias_para_entrega"] <= 7).sum() / len(df_filtrado)
) * 100 if len(df_filtrado) > 0 else 0

# 4. Exibição nos 4 Cartões
col1, col2, col3, col4 = st.columns(4)

with col1:
    with st.container(border=True):
        st.metric(
            label="💰 Faturamento Total",
            value=formatar_numero(receita_total, prefixo="R$ "),
            delta=f"Frete: {frete_pct:.1f}% da receita",
            delta_color="off",
        )
with col2:
    with st.container(border=True):
        st.metric(
            label="📦 Total de Pedidos",
            value=formatar_numero(total_pedidos),
            delta=f"Média de {itens_por_pedido:.1f} itens / pedido",
            delta_color="off",
        )
with col3:
    with st.container(border=True):
        st.metric(
            label="🎟️ Ticket Médio",
            value=formatar_numero(ticket_medio, prefixo="R$ "),
            delta=f"Parcelamento médio: {parcelas_media:.1f}x",
            delta_color="off",
        )
with col4:
    with st.container(border=True):
        st.metric(
            label="🚚 Tempo Médio Entrega",
            value=f"{tempo_medio_entrega:.1f} dias",
            delta=f"{entrega_rapida_pct:.1f}% entregues em até 7 dias",
            delta_color="off",
        )

# ==============================================================================
# 6. ABAS DE NAVEGAÇÃO (VISUAL APP-LIKE)
# ==============================================================================
aba_vendas, aba_logistica = st.tabs(
    ["📊 Performance de Vendas", "🚚 Análise Logística"]
)

# --- ABA 1: PERFORMANCE DE VENDAS ---
with aba_vendas:
    col_graf1, col_graf2 = st.columns(2)

    with col_graf1:
        with st.container(border=True):
            st.markdown("#### 📈 Receita Mensal")
            vendas_mensais = (
                df_filtrado.groupby("ano_mes")["preco_produto"]
                .sum()
                .reset_index()
            )

            fig_evolucao = px.area(
                vendas_mensais,
                x="ano_mes",
                y="preco_produto",
                color_discrete_sequence=["#38bdf8"],
            )
            fig_evolucao.update_layout(
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                margin=dict(l=10, r=10, t=10, b=10),
                xaxis=dict(title=None, showgrid=False),
                yaxis=dict(title=None, showgrid=True, gridcolor="#1f2937"),
                hovermode="x unified",
            )
            fig_evolucao.update_traces(
                line=dict(width=3),
                hovertemplate="R$ %{y:,.2f}",
            )
            st.plotly_chart(fig_evolucao, width="stretch")

    with col_graf2:
        with st.container(border=True):
            st.markdown("#### 🏆 Top 10 Categorias")
            top_categorias = (
                df_filtrado.groupby("categoria_produto")["preco_produto"]
                .sum()
                .reset_index()
                .sort_values(by="preco_produto", ascending=False)
                .head(10)
            )

            fig_categorias = px.bar(
                top_categorias,
                x="preco_produto",
                y="categoria_produto",
                orientation="h",
                color_discrete_sequence=["#0ea5e9"],
            )
            fig_categorias.update_layout(
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                yaxis=dict(
                    title=None,
                    categoryorder="total ascending",
                    showgrid=False,
                ),
                xaxis=dict(title=None, showgrid=True, gridcolor="#1f2937"),
                margin=dict(l=10, r=10, t=10, b=10),
            )
            fig_categorias.update_traces(
                hovertemplate="Receita: R$ %{x:,.2f}",
            )
            st.plotly_chart(fig_categorias, width="stretch")

# --- ABA 2: ANÁLISE LOGÍSTICA ---
with aba_logistica:
    with st.container(border=True):
        st.markdown("#### 📦 Tempo Médio de Entrega por Estado (Dias)")
        entrega_estado = (
            df_filtrado.groupby("estado_cliente")["dias_para_entrega"]
            .mean()
            .reset_index()
            .sort_values(by="dias_para_entrega", ascending=True)
        )

        fig_entrega = px.bar(
            entrega_estado,
            x="estado_cliente",
            y="dias_para_entrega",
            color="dias_para_entrega",
            color_continuous_scale="Blues",
        )
        fig_entrega.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(title="Estado", showgrid=False),
            yaxis=dict(
                title="Dias Média", showgrid=True, gridcolor="#1f2937"
            ),
            margin=dict(l=10, r=10, t=10, b=10),
            coloraxis_showscale=False,
        )
        st.plotly_chart(fig_entrega, width="stretch")