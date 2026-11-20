---
title: Delivery Insights
emoji: 📊
colorFrom: red
colorTo: red
sdk: streamlit
sdk_version: 1.30.0
app_file: app.py
pinned: false
---

# 📊 Delivery Insights com Inteligência Artificial

Este dashboard foi desenvolvido para simular um ambiente de análise de dados de operações logísticas de delivery. O objetivo é extrair insights acionáveis sobre **tempo de entrega, satisfação do cliente e eficiência operacional**, utilizando Inteligência Artificial para gerar recomendações de negócio.

## 🎯 O Problema de Negócio
Gestores de operações de delivery precisam lidar diariamente com variáveis complexas (trânsito, clima, tempo de preparo dos restaurantes) que impactam diretamente a satisfação do cliente e o custo operacional. Identificar o "gargalo" manualmente em milhares de pedidos é lento e suscetível a erros.

## 💡 A Solução
Um pipeline de dados automatizado em Python que:
1. **Ingere e Limpa** os dados brutos (ETL).
2. **Visualiza** as correlações e hipóteses de negócio através de gráficos interativos.
3. **Gera um Relatório Executivo** automático usando um LLM (Large Language Model), que valida hipóteses, encontra a causa raiz dos atrasos e propõe um plano de ação prático.

## 🛠️ Tecnologias Utilizadas
* **Python:** Linguagem base.
* **Pandas:** Tratamento, limpeza e engenharia de dados.
* **Streamlit:** Criação do dashboard interativo e responsivo.
* **Plotly Express:** Visualização de dados dinâmica e customizada (Dark Mode).
* **Groq API (Modelo GPT-OSS-120B):** Geração de insights e relatórios executivos em tempo real.

## 📊 Metodologia (ETL e Análise)
1. **Extração:** Base de dados simulada com 50.000 registros extraída do Kaggle.
2. **Transformação:**
   * Tradução e padronização de colunas para o português (pt-BR).
   * Tratamento de dados nulos e remoção de duplicatas (`dropna` e `drop_duplicates`).
   * Tradução de valores categóricos (ex: `Clear` -> `Limpo`, `High` -> `Alto`).
   * Padronização de decimais (vírgula) e formatação monetária (R$).
3. **Análise:**
   * Levantamento de hipóteses de negócio.
   * Análise de correlação (Matriz de Pearson) para encontrar as variáveis que mais impactam o tempo de entrega.
   * Storytelling de dados.

## 🚀 Como Executar Localmente
1. Clone o repositório.
2. Instale as dependências:
   ```bash
   pip install -r requirements.txt