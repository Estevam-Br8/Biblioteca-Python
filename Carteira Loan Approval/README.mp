# 🏦 CrediNova Bank — Executive Credit & Risk Analytics

[![Power BI](https://img.shields.io/badge/Power_BI-Executive_Dashboard-F2C811.svg?logo=powerbi&logoColor=black)](https://powerbi.microsoft.com/)
[![Python](https://img.shields.io/badge/Python-3.11%2B-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![Pandas](https://img.shields.io/badge/Pandas-ETL%20%26%20Data%20Marts-150458.svg?logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![NumPy](https://img.shields.io/badge/NumPy-Mathematical%20Assets-013243.svg?logo=numpy&logoColor=white)](https://numpy.org/)
[![Pillow](https://img.shields.io/badge/Pillow-Animated%20UI%20Engine-4B8BBE.svg)](https://python-pillow.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

> **Visão executiva interativa de análise de carteira, esteira de risco e perfil demográfico de crédito do CrediNova Bank, combinando engenharia de dados em Python, geração matemática de assets visuais e dashboarding avançado no Power BI.**

---

## 🎯 O Problema de Negócio

Em instituições financeiras e fintechs de crédito, o crescimento sustentável da carteira exige o equilíbrio exato entre **expansão de volume financeiro** e **rigoroso controle de risco**. Analisar a concessão de empréstimos em tabelas isoladas impede que a diretoria visualize os gargalos da esteira de aprovação e o real perfil socioeconômico dos tomadores.

O projeto do **CrediNova Bank** foi desenvolvido para responder a perguntas estratégicas em tempo real:
* 💰 **Qual é a composição da carteira por finalidade de empréstimo e onde está concentrado o volume financeiro?**
* ⚖️ **Qual é o impacto direto da faixa de *Credit Score* e da exigência de garantia (*Secured* vs *Unsecured*) na taxa de recusa de propostas?**
* 🏷️ **Como a taxa média de juros (9,26%) é precificada entre os diferentes perfis de risco?**
* 👤 **Quem é o tomador de crédito (renda média anual, nível educacional, empregabilidade e ticket médio solicitado)?**

---

## 🧠 Bastidores do Desenvolvimento & Decisões de Arquitetura

O desenvolvimento desta solução foi desenhado para simular o ciclo de vida completo de um projeto de **Business Intelligence Moderno**, integrando Engenharia de Dados (Python), Design Sistemático (UI/UX) e Modelagem Analítica (Power BI).

Abaixo estão os pilares e as escolhas técnicas que guiaram a construção do projeto:

### 1️⃣ Arquitetura em Data Marts Específicos
Em vez de carregar um único arquivo monolítico e sobrecarregar o modelo em memória no Power BI, a base bruta (*Loan Approval Dataset* — 52.000 registros) foi agregada e transformada via scripts em três **Data Marts temáticos**:
* `01_visao_executiva.csv`: Métricas de volume, ticket médio e aprovação agrupadas por finalidade do empréstimo.
* `02_visao_risco.csv`: Cruzamento de faixas de *Credit Score*, presença de garantia, taxas de rejeição e precificação de juros.
* `03_visao_perfil.csv`: Mapeamento socioeconômico unindo nível educacional, status ocupacional, idade e renda anual.
* **Benefício:** Redução drástica no tempo de renderização do relatório e isolamento de contexto para consultas executivas rápidas.

### 2️⃣ Automação Visual via Script Python (`script/gerar_fundo.py`)
* Para elevar o padrão visual (*UI/UX*) do dashboard sem depender de ferramentas pagas de design, utilizou-se um script em **Python (`NumPy` + `Pillow`)** para gerar matematicamente um fundo animado em `.gif` (*Fluxo Contínuo* em tom `#F3F4F6`).
* **Matemática aplicada:** Cálculo de ondas senoidais diagonais com transições suaves de fase em 60 frames em *loop* infinito, simulando o efeito de varredura/esteira de dados sem gerar fadiga visual ou distração.

### 3️⃣ Normalização e Modelagem DAX Ponderada
* **Padrões de Varejo Bancário:** No Power Query, os percentuais brutos exportados do SQL/Python foram normalizados (divisão por 100) para permitir formatação nativa de porcentagem com precisão decimal no Power BI.
* **Métricas Ponderadas:** Criação de medidas em DAX para calcular a **Taxa de Rejeição Geral Real (35,83%)** e **Taxa de Juros Ponderada (9,26%)** com base no peso do volume de propostas por categoria, evitando distorções causadas por médias simples.

### 4️⃣ UI/UX & Design Sistemático Executivo
* **Layout em Grid/Cards:** Utilização de caixas com bordas suavizadas e sombras sutis (*Glassmorphism léger*) para separar métricas operacionais dos gráficos analíticos.
* **Paleta de Cores Funcional:** Uso estratégico de cores de contraste (Verde para aprovação/baixo risco, Laranja/Amarelo para risco moderado e Vermelho para alto risco).

---

## 🏗️ Fluxo Geral do Pipeline

```text
[ Kaggle API / Base Bruta CSV ]
               │
               ▼
   ( Scripts de Tratamento )   ──► Limpeza, agregação e criação dos Data Marts
               │
               ├───► [ 01_visao_executiva.csv ] ──► (Data Mart: Carteira & Finalidades)
               ├───► [ 02_visao_risco.csv ]     ──► (Data Mart: Score, Garantias & Juros)
               └───► [ 03_visao_perfil.csv ]    ──► (Data Mart: Demografia & Renda)
               │
   ( script/gerar_fundo.py )   ──► Processamento matemático (NumPy + Pillow)
               │
               ▼
    [ fundo_fluxo.gif ]        ──► Renderização do canvas animado
               │
               └─────────────────────────────┐
                                             ▼
                                  [ Power BI Desktop ]
                                             │
               ┌─────────────────────────────┼─────────────────────────────┐
               ▼                             ▼                             ▼
   (Pág 1: Visão Executiva)     (Pág 2: Análise de Risco)    (Pág 3: Perfil Demográfico)
