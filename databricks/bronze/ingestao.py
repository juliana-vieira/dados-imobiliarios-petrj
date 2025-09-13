# Databricks notebook source
# DBTITLE 1,SETUP
import sys

sys.path.insert(0, "../lib/") # Obtenção dos módulos da pasta lib

import ingestors
import db

# Definição de atributos
table = 'imoveis'
catalog = 'bronze'
database = 'olx'
idField = 'cod_anuncio'
checkpoint_path = f"/Volumes/raw/lh-projeto-olx/full-load/checkpoints/"

# Configuração do timestamp para UTC-3 (horário de Brasília)
spark.conf.set("spark.sql.session.timeZone", "America/Sao_Paulo")

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
