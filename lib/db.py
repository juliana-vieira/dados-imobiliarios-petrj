# Funções auxiliares que serão usadas na ingestão

# Importa queries de arquivos especificados no path
def import_query(path):
    with open(path, 'r') as f:
        return f.read()

# Verifica se a tabela já existe no catálogo e retorna o valor caso o count seja True (maior que 0)
def table_exists(catalog, database, table, spark):
    count = (spark.sql(f"SHOW TABLES FROM {catalog}.{database}")
                  .filter(f"database = '{database}'")
                  .filter(f"tableName = '{table}'")
                  .count())
    
    return count > 0