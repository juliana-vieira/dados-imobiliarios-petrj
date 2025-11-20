# Databricks notebook source
# DBTITLE 1,SETUP
# MAGIC %pip install ../../lib/
# MAGIC # Instalação dos módulos ingestors.py e db.py da pasta lib
# MAGIC
# MAGIC import ingestors
# MAGIC import db 
# MAGIC
# MAGIC # Definição de atributos
# MAGIC table = 'imoveis'
# MAGIC catalog = 'bronze'
# MAGIC database = 'olx'
# MAGIC idField = 'cod_anuncio'
# MAGIC checkpoint_path = f"/Volumes/raw/lh-projeto-olx/full-load/checkpoints/"
# MAGIC
# MAGIC # Configuração do timestamp para UTC-3 (horário de Brasília)
# MAGIC spark.conf.set("spark.sql.session.timeZone", "America/Sao_Paulo")

# COMMAND ----------

# DBTITLE 1,INGESTÃO FULL LOAD (BATCH)
# Verificação da existência da tabela no catálogo
# Se não existir, cria com a classe de ingestão em batch

if not db.table_exists(catalog, database, table, spark):
    print("Criando a tabela...")
    ingestao = ingestors.IngestaoFullBronze(table, idField, spark)
    ingestao.auto()
    dbutils.fs.rm(checkpoint_path, True)

    print(f"Tabela {catalog}.{table} criada com sucesso.")

# COMMAND ----------

# DBTITLE 1,INGESTÃO FULL LOAD (STREAM)
# Execução streaming

print("Executando stream...")
ingestao = ingestors.IngestaoFullBronzeStreaming(table, idField, spark)
ingestao.auto()

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC SELECT DISTINCT * FROM bronze.olx.imoveis
