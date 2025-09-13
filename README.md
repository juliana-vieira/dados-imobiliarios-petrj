# 🏠 Dados Imobiliários de Petrópolis/RJ

## 📋 Sobre o Projeto

Este projeto tem como objetivo **analisar o mercado imobiliário de Petrópolis-RJ** por meio de um pipeline completo de dados. A coleta é realizada via **web scraping** em Python, orquestrada pelo **Prefect**. Os dados são processados e armazenados em um **Data Lakehouse no Databricks**, com a arquitetura em camadas bronze, silver e gold, utilizando **streaming com PySpark**. Por fim, um **dashboard interativo no Streamlit** possibilita a análise e visualização das informações.

### 🎯 Objetivos
- Coletar dados imobiliários de Petrópolis/RJ de forma automatizada
- Implementar pipeline de dados escalável e monitorado
- Analisar tendências do mercado imobiliário local

---

## Status do Projeto

**🔄 EM DESENVOLVIMENTO**

### ✅ **Implementado:**

**Web scraping com Python e orquestrador Prefect**
- Extração automatizada de imóveis para alugar, com agendamento no Prefect local e upload dos dados no S3

**Lakehouse no Databricks** - Implementação de arquitetura em camadas
   - 🥉 **Bronze**: Consumo dos dados brutos do S3, pequenas transformações na estrutura da delta e ingestão no Unity Catalog com streaming.

### **Próximos Passos:**
   - Extração de dados de imóveis à venda
   - 🥈 **Silver**: Dados limpos e padronizados  
   - 🥇 **Gold**: Dados agregados prontos para análise
   
   **Dashboard Streamlit** - Interface de análise
   - Visualizações interativas dos dados
   - Métricas do mercado imobiliário
   - Filtros por região, tipo de imóvel e faixa de preço

---

## 📊 Dados Coletados

### **Informações dos Imóveis:**
- **Tipo**: Casas e apartamentos
- **Preço**: Venda e aluguel
- **Localização**: Bairro, endereço
- **Características**: Área, quartos, banheiros, vagas
- **Extras**: Condomínio, IPTU, descrição completa

---
