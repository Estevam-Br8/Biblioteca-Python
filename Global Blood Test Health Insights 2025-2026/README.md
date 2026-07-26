# 🩸 Global Blood Test Health Insights — Pipeline ETL & Data Analytics

[![Python](https://img.shields.io/badge/Python-3.13%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Pandas](https://img.shields.io/badge/Pandas-Data%20Manipulation-150458?logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![PyArrow](https://img.shields.io/badge/PyArrow-Parquet%20Storage-2D0000?logo=apache&logoColor=white)](https://arrow.apache.org/)
[![Kaggle API](https://img.shields.io/badge/Kaggle-API%20Ingestion-20BEFF?logo=kaggle&logoColor=white)](https://www.kaggle.com/)

Projeto de **Engenharia de Dados End-to-End** focado no consumo automatizado de APIs, tratamento/limpeza de dados médicos e geração de relatórios de saúde. O pipeline foi desenvolvido seguindo arquitetura modular e boas práticas de armazenamento colunar (Apache Parquet).

---

## 🎯 Objetivo do Projeto

Transformar dados brutos de exames de sangue globais em uma **camada de dados otimizada e pronta para análise (Analytical Layer)**, permitindo identificar padrões demográficos e biomarcadores críticos de saúde de forma automatizada e escalável.

---

## 🏗️ Arquitetura do Pipeline

O pipeline foi projetado de forma **modular e desacoplada**, garantindo fácil manutenção, isolamento de falhas e capacidade de reuso:

```text
Global Blood Test Health Insights/
│
├── dados/
│   ├── base/           # [Raw Data / Landing Zone] CSVs brutos vindos da API
│   └── processados/    # [Processed / Gold Zone] Arquivos Parquet otimizados
│
├── Script python/
│   ├── 01_import_api.py # Ingestão via API Kaggle (Extração)
│   ├── 02_etl.py        # Limpeza, transformação e escrita colunar (ETL)
│   └── 03_analysis.py   # Análise exploratória e KPIs (Analytics)
│
├── README.md            # Documentação técnica do repositório
└── requirements.txt     # Dependências do ambiente
