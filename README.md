# Pipeline ETL de Dados Globais (REST Countries API) 🌍

Este é o **Projeto 1** de uma série de projetos práticos focados em Engenharia de Dados. O objetivo principal deste desafio foi construir uma pipeline local de ingestão, tratamento e carga de dados (ETL) utilizando boas práticas de mercado, como isolamento de ambiente e armazenamento colunar.

## 📌 Arquitetura & Fluxo do Dado (Data Lake Local)

A estrutura simula a organização de um Data Lake básico dividido em camadas:

1. **Extract (Extração):** O script consome dados reais da API pública [REST Countries](https://restcountries.com/). Para garantir resiliência contra instabilidades no servidor (erros HTTP 400), a extração foi desenhada para buscar dados em lotes divididos por regiões continentais. O dado bruto (JSON) é salvo na camada **Raw (Bronze)**.
2. **Transform (Transformação):** Utilizando a biblioteca **Pandas**, o JSON complexo e aninhado é processado. Filtramos apenas as colunas essenciais, tratamos valores ausentes/nulos, removemos registros duplicados e ordenamos os dados.
3. **Load (Carga):** A tabela tratada é convertida e salva na camada **Processed (Silver)** utilizando o formato **Parquet** (compactado e colunar), otimizando o espaço em disco e mantendo os metadados dos tipos de dados.

---

## 🛠️ Tecnologias e Ferramentas Utilizadas

* **Python 3** (Linguagem core)
* **Requests** (Consumo da API HTTP)
* **Pandas** (Manipulação e tratamento de dados)
* **PyArrow** (Engine para conversão e escrita de arquivos Parquet)
* **Git & GitHub** (Controle de versão)

---

## 📁 Estrutura do Projeto

```text
pipeline-paises/
├── data/
│   ├── raw/           # Camada Bronze: JSON bruto original
│   └── processed/     # Camada Silver: Parquet limpo e tratado
├── .gitignore         # Arquivos ignorados pelo Git (ex: .venv, data/)
├── pipeline.py        # Script principal do ETL
└── requirements.txt   # Dependências do projeto
