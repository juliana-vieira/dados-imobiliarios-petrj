# 🏠 Dados Imobiliários de Petrópolis/RJ

## 📋 Sobre o Projeto

Este projeto tem como objetivo **analisar o cenário imobiliário de Petrópolis, RJ** através da coleta automatizada de dados utilizando técnicas de **web scraping**. A solução implementa um pipeline robusto de extração de dados orquestrado pelo **Prefect**, coletando informações de imóveis anunciados na OLX para análises do mercado local.

### 🎯 Objetivos
- Coletar dados imobiliários de Petrópolis/RJ de forma automatizada
- Implementar pipeline de dados escalável e monitorado
- Analisar tendências do mercado imobiliário local

---

## Status do Projeto

**🔄 EM DESENVOLVIMENTO**

### ✅ **Implementado:**

**Web scraping com Python e orquestrador Prefect**
- Extração automatizada de dados imobiliários com agendamento no Prefect local

**Lakehouse no Databricks** - Implementação de arquitetura em camadas
   - 🥉 **Bronze**: Dados brutos com pequenas transformações na estrutura da delta

### **Próximos Passos:**
   - 🥈 **Silver**: Dados limpos e padronizados  
   - 🥇 **Gold**: Dados agregados prontos para análise
   
   **Dashboard Streamlit** - Interface de análise
   - Visualizações interativas dos dados
   - Métricas do mercado imobiliário
   - Filtros por região, tipo de imóvel e faixa de preço

---

## 📊 Dados Coletados

### **Informações dos Imóveis:**
- 🏠 **Tipo**: Casas e apartamentos
- 💰 **Preço**: Venda e aluguel
- 📍 **Localização**: Bairro, endereço
- 📐 **Características**: Área, quartos, banheiros, vagas
- 🏢 **Extras**: Condomínio, IPTU, descrição completa
  
---