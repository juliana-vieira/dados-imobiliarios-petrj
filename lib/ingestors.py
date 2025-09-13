import delta
import db
from pyspark.sql.functions import current_timestamp

# Classe para ingestão Full Load em batch
class IngestaoFullBronze:
    def __init__(self, table, idField, spark):
        self.table = table
        self.idField = idField
        self.tablename = f'bronze.olx.{self.table}' # Definição do nome da tabela dentro do catalog.database
        self.path = "/Volumes/raw/lh-projeto-olx/full-load/raw/" # Caminho dos arquivos raw
        self.query = db.import_query(f"{self.table}.sql") # Importação da query do arquivo imoveis.sql utilizando o método import_query do módulo db.py
        self.spark = spark

    def read(self):

        # Leitura dos arquivos
        df = self.spark.read.json(self.path)
        return df
    
    def transform(self, df):
        # Método que executa as transformações necessárias no dataframe para preparar para ingestão

        # Criação da VIEW temporária para transformação com SQL
        df.createOrReplaceTempView(self.table)

        # Execução da query armazenada em self.query na tabela armazenada em self.table
        # Essa query explode as colunas com json aninhado e converte as colunas com listas em arrays de strings
        df = self.spark.sql(self.query.format(table = self.table)) 

        # Adição de uma coluna com a data e hora da ingestão em UTC-3 ao df
        df = df.withColumn("ingestion_time", current_timestamp())   
              
        return df
    
    def save(self, df):
       # Método que salva o dataframe em delta com overwrite completo (dados e schema) em bronze.olx.imoveis

        (df.write
              .format("delta")
              .mode("overwrite")
              .option("overwriteSchema", "true")
              .saveAsTable(self.tablename))

    def auto(self):
        # Método que executa todas as etapas anteriores
        
        df = self.read()
        df_transform = self.transform(df)
        self.save(df_transform)

# Classe de ingestão Full Load com streaming que herda da classe IngestaoFullBronze
class IngestaoFullBronzeStreaming(IngestaoFullBronze):
       def __init__(self, table, idField, spark):
              super().__init__(table, idField, spark)

              # Definição do checkpoint_path, onde serão a armazenadas as informações utilizadas pela streams
              # Por que usar streaming? -> Evita reprocessamento de arquivos. Se o bucket possuir 1000 arquivos, a stream não vai processar todos a cada execução, e sim os arquivos
              # que não estão presentes nos metadados do checkpoint
              # Essas informações são necessárias para que a stream saiba em qual posição parou a última execução, ou seja, somente arquivos novos serão processados
              self.checkpoint_path = "/Volumes/raw/lh-projeto-olx/full-load/checkpoints/" 
       
       def read(self):
           # Stream de leitura

           # Retorna um dataframe do Databricks AutoLoader 
           # O AutoLoader identifica automaticamente arquivos novos em nuvem, sem necessidade de gerenciamento manual
             return (self.spark.readStream
                               .format("cloudFiles")
                               .option("cloudFiles.format", "json")
                               .option("cloudFiles.schemaLocation", f"{self.checkpoint_path}/schema")
                               .load(self.path))     

       def transform(self, df, batch_id):
           # Método de transformação em batch, similar ao método transform de IngestaoFullBronze

            df.createOrReplaceTempView(self.table)

            df = self.spark.sql(self.query.format(table = self.table))      
            df = df.withColumn("ingestion_time", current_timestamp()) 

            # Remoção de duplicatas antes do MERGE
            # Como o dataset não possui uma coluna com a data de atualização, a deduplicação é feita pelo id do anúncio
            df = df.dropDuplicates([self.idField])
            
            # Criação de uma tabela delta com a tabela que está armazenada no catálogo atualmente (bronze.olx.imoveis)
            delta_table = delta.DeltaTable.forName(self.spark, self.tablename)
            join_on = f"t.{self.idField} = d.{self.idField}"

            # Mesclagem dos dados novos com os dados da delta
            # Isso atualiza os dados com base no id do anúncio
            # Se o id do anúncio não existir na tabela atual, ele é inserido
            (delta_table.alias("d")
                        .merge(df.alias("t"), join_on)
                        .whenMatchedUpdateAll()
                        .whenNotMatchedInsertAll()
                        .execute())

       def save(self, df):
           # Stream de escrita

           # Executa o método transform para cada batch da stream
           # o trigger availableNow processa todos os dados disponíveis e encerra automaticamente quando a stream finaliza
              (df.writeStream
                        .foreachBatch(self.transform)
                        .option("checkpointLocation", f"{self.checkpoint_path}/bronze_{self.table}")
                        .trigger(availableNow=True)
                        .start())

       def auto(self):
           # Método que executa todas as etapas anteriores

              df = self.read()
              self.save(df)