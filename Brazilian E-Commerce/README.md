# 🛍️ Brazilian E-Commerce Executive Analytics (Code-First BI)

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://biblioteca-java-vticaupwgmdqssgvzjl8vm.streamlit.app/)
[![Python](https://img.shields.io/badge/Python-3.11%2B-blue.svg)](https://www.python.org/)
[![Pandas](https://img.shields.io/badge/Pandas-ETL%20%26%20Data%20Prep-150458.svg)](https://pandas.pydata.org/)
[![SQLite](https://img.shields.io/badge/SQLite-Relational%20DB-003B57.svg)](https://www.sqlite.org/)
[![Plotly](https://img.shields.io/badge/Plotly-Interactive%20Charts-3F4F75.svg)](https://plotly.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

> **Visão executiva interativa de vendas e nível de serviço logístico de E-Commerce brasileiro, desenvolvida sob a metodologia Code-First BI (100% código, sem ferramentas Low-Code proprietárias).**

---

## 🟢 Acesso Rápido ao Dashboard Online

O projeto está publicado em nuvem e pode ser acessado de qualquer dispositivo sem necessidade de login ou instalação:

👉 **[CLIQUE AQUI PARA TESTAR O WEB APP INTERATIVO](https://biblioteca-java-vticaupwgmdqssgvzjl8vm.streamlit.app/)**

---

## 📸 Prévia do Projeto (Screenshots)

O aplicativo foi desenhado no estilo **App-Like / SaaS Moderno**, se adaptando tanto ao **Dark Mode** quanto ao **Light Mode** e evitando a poluição visual dos relatórios tradicionais:

| **Visão Geral & KPIs Executivos** | **Navegação por Abas (Vendas vs. Logística)** |
| :---: | :---: |
| <img src="https://placehold.co/600x320/1e293b/38bdf8?text=Dashboard+%2B+Cards+de+KPI" width="100%" alt="Prévia do Dashboard"> | <img src="https://placehold.co/600x320/1e293b/38bdf8?text=Abas+%2B+Gr%C3%A1ficos+Plotly" width="100%" alt="Prévia das Abas"> |
* *(Dica: Você pode substituir os placeholders acima colocando imagens reais na pasta do projeto ou linkando prints gravados no GitHub)*.

---

## 🎯 O Problema de Negócio

No varejo digital brasileiro, o crescimento sustentável depende do equilíbrio entre **receita** e **eficiência operacional**. Painéis tradicionais muitas vezes separam os números financeiros da performance logística, dificultando a visão sistêmica da diretoria.

Este projeto visa responder a perguntas críticas executivas em tempo real:
* 💰 **Qual é o peso do frete sobre o faturamento total dos produtos?**
* 📦 **Qual é o comportamento do carrinho (quantidade média de itens por pedido)?**
* 🎟️ **Como o cliente brasileiro utiliza o crédito (parcelamento médio no cartão)?**
* 🚚 **Qual é o tempo real de entrega por estado e a porcentagem de entregas expressas (SLA $\le$ 7 dias)?**

---

## 🧠 Bastidores do Desenvolvimento & Decisões de Arquitetura

O desenvolvimento deste projeto foi pensado para simular o dia a dia de um **Engenheiro de Dados / Analista de BI Moderno** trabalhando com versionamento Git, controle de qualidade de código e automação de pipelines. 

Abaixo estão os pilares e as escolhas técnicas que guiaram a construção da solução:

### 1️⃣ Abordagem Code-First BI vs. Low-Code
Em vez de utilizar soluções baseadas em "arrastar e soltar" (como Power BI ou Tableau), optou-se pela **criação de uma aplicação web nativa em Python**.
* **Por quê?** O Code-First BI garante **total controle de versão (Git)**, facilita auditorias linha a linha no código, elimina custos de licenças para compartilhamento externo e permite integração contínua (CI/CD) com pipelines de ciência de dados e machine learning.

### 2️⃣ Ingestão Automatizada e Resiliente (`01_import_api.py`)
* Em vez de baixar planilhas manualmente no navegador, o script utiliza a biblioteca oficial `kagglehub` conectada à API do Kaggle para baixar a base pública da *Olist* (8 tabelas relacionais em `.csv`).
* **Inteligência no script:** O código verifica a existência de arquivos na pasta de destino (`dados/base/`) antes de agir, oferecendo ao usuário um menu interativo no terminal para substituir ou abortar a operação sem desperdiçar banda ou sobrescrever dados sem aviso.

### 3️⃣ Pipeline ETL & Modelagem Relacional (`02_etl.py`)
* **Limpeza e Cruzamento:** Utilizando `Pandas` e `NumPy`, o script cruza as tabelas de pedidos, itens, produtos, clientes, pagamentos e traduções.
* **Regras de Negócio Injetadas:**
  * Cálculo dinâmico de SLA logístico (`dias_para_entrega = data_entrega - data_compra`).
  * Segmentação de produtos por faixas de preço no padrão varejo (*Entrada*, *Intermediário* e *Premium*).
  * Agregação e higienização de meios de pagamento e parcelamentos.
* **Dupla Estratégia de Saída:** Ao final da transformação, o script exporta os dados limpos em formato **Parquet** (alta compressão e velocidade analítica) e grava tudo em um banco de dados **SQLite3 (`ecommerce_analytics.db`)**, possibilitando consultas SQL nativas.

### 4️⃣ Interface, Performance e Resiliência (`dashboard/app.py` + `style.css`)
* **Consulta SQL Otimizada:** O aplicativo executa uma query SQL direta no banco `.db` e utiliza `@st.cache_data` para manter a base carregada em memória, fazendo com que filtros dinâmicos respondam em milissegundos.
* **Fallbacks e Proteção de Erros:** O código conta com lógicas de proteção (`try/except` e checagens de colunas) para garantir que o painel continue funcionando perfeitamente, mesmo que o banco de dados seja atualizado ou testado com versões parciais dos dados.

---

## 🏗️ Fluxo Geral do Pipeline

```text
[ API Kaggle / Olist ] 
        │
        ▼
 (01_import_api.py)  ──► Download automatizado de arquivos CSV brutos
        │
        ▼
    (02_etl.py)      ──► Tratamento, conversões de datas e joins em Pandas
        │
        ├─────────────────────────────┐
        ▼                             ▼
 [ v_vendas.parquet ]      [ ecommerce_analytics.db ]  ──► (SQLite Relacional)
                                      │
                                      ▼
                               (dashboard/app.py)      ──► (Streamlit + Plotly Web App)
